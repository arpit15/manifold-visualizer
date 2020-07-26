import copy
from misc import *
from path import *
from draw import *
from mode import Mode
from knob import DraggableKnob
from nanogui import *

class SpecularManifoldSamplingMode(Mode):
    def __init__(self, viewer):
        super().__init__(viewer)

        self.seed_path = None
        self.solution_path = None

        self.constraint_type = ConstraintType.HalfVector
        self.strategy_type = StrategyType.SMS

        self.dragging_start = False
        self.dragging_end   = False
        self.dragging_spec  = False
        self.knob_start = DraggableKnob()
        self.knob_end   = DraggableKnob()
        self.knob_spec  = DraggableKnob()

        self.normal_distr = None
        self.solution_paths = []

        self.animating = False
        self.time = 0.0
        self.scene = None
        self.animation_state = 0

    def scene_changed(self):
        scene = self.viewer.scenes[self.viewer.scene_idx]
        self.n_bounces_box.set_value(scene.n_bounces_default)

    def update(self, input, scene):
        super().update(input, scene)
        self.scene = scene

        if self.animating:
            self.time += 0.02
            time_p = 0.5 + 0.5*np.sin(self.time)

            self.roughness_sl.set_value(time_p)

        # Set positions and update for all three knobs
        p_start = scene.sample_start_position(scene.start_u_current).p
        p_end = scene.sample_end_position(scene.end_u_current).p
        p_spec = scene.sample_spec_position(scene.spec_u_current).p
        self.knob_start.p = copy.copy(p_start)
        self.knob_end.p = copy.copy(p_end)
        self.knob_spec.p = copy.copy(p_spec)

        self.knob_start.update(input)
        if input.click and (self.knob_start.drag_possible or self.dragging_start):
            self.dragging_start = True
            p_start += input.mouse_dp
        else:
            self.dragging_start = False
        u_proj = scene.start_shape().project(p_start)
        scene.start_u_current = u_proj

        self.knob_end.update(input)
        if input.click and (self.knob_end.drag_possible or self.dragging_end):
            self.dragging_end = True
            p_end += input.mouse_dp
        else:
            self.dragging_end = False
        u_proj = scene.end_shape().project(p_end)
        scene.end_u_current = u_proj

        self.knob_spec.active = self.strategy_type == StrategyType.SMS
        self.knob_spec.update(input)
        if input.click and (self.knob_spec.drag_possible or self.dragging_spec):
            self.dragging_spec = True
            p_spec += input.mouse_dp
        else:
            self.dragging_spec = False
        u_proj = scene.first_specular_shape().project(p_spec)
        scene.spec_u_current = u_proj

        if self.strategy_type == StrategyType.MNEE:
            self.seed_path = scene.sample_mnee_seed_path()
        else:
            self.seed_path = scene.sample_seed_path(self.n_bounces_box.value())

        if self.seed_path.has_specular_segment():
            self.solution_path, _ = self.newton_solver(scene, self.seed_path)


        # Roughness
        def gauss(x, mu, sigma):
            return 1/(sigma*np.sqrt(2*np.pi)) * np.exp(-0.5*((x-mu)/sigma)**2)

        alpha = 0.005 + (0.2 - 0.005)*self.roughness_sl.value()
        mu = 0.0
        sigma2 = 0.5*alpha*alpha
        M = 1000
        dx = 4*np.sqrt(sigma2)

        # Slope range
        xx = np.linspace(-dx, +dx, M)
        yy = gauss(xx, mu, sigma2)

        # Convert slopes to normals
        nn = np.zeros((M, 2))
        nn[:,0] = -xx
        nn[:,1] = 1
        norms = np.sqrt(nn[:,0]**2 + 1)
        nn[:,0] /= norms
        nn[:,1] /= norms

        # Run Newton solver for both "extreme ends"
        seed_path = self.seed_path.copy()
        self.solution_paths = []
        if seed_path.has_specular_segment():

            for n_offset in [nn[0,:], nn[-1,:]]:
                for k, vtx in enumerate(seed_path):
                    if vtx.shape.type == Shape.Type.Reflection or vtx.shape.type == Shape.Type.Refraction:
                        vtx.n_offset = n_offset

                solution_path, _ = self.newton_solver(self.scene, seed_path)
                if solution_path:
                    self.solution_paths.append(solution_path.copy())

        # Scale normals with contribution from gaussian for drawing the lobe later
        scale = yy / np.max(yy)
        nn[:,0] *= scale*20      # Draw the lobe much wider s.t. it looks more interesting
        nn[:,1] *= scale

        self.normal_distr = nn


    def newton_solver(self, scene, seed_path):
        current_path = seed_path.copy()
        intermediate_paths = [current_path]

        i = 0
        beta = 1.0
        N = self.max_steps()
        threshold = self.eps_threshold()
        success = False
        while True:
            # Give up after too many iterations
            if i >= N:
                break

            # Compute tangents and constraints
            current_path.compute_tangent_derivatives(self.constraint_type)
            if current_path.singular:
                break

            # Check for success
            converged = True
            for vtx in current_path:
                if vtx.shape.type == Shape.Type.Reflection or vtx.shape.type == Shape.Type.Refraction:
                    if abs(vtx.C) > threshold:
                        converged = False
                        break
            if converged:
                success = True
                break

            proposed_offsets = current_path.copy_positions()
            for k, vtx in enumerate(current_path):
                if vtx.shape.type == Shape.Type.Reflection or vtx.shape.type == Shape.Type.Refraction:
                    proposed_offsets[k] -= beta * vtx.dp_du * vtx.dX

            # Ray trace to re-project onto specular manifold
            proposed_path = scene.reproject_path_sms(proposed_offsets, current_path, self.n_bounces_box.value())
            if not current_path.same_submanifold(proposed_path):
                beta = 0.5 * beta
            else:
                beta = min(1.0, 2*beta)
                current_path = proposed_path
                intermediate_paths.append(current_path)

            i = i + 1

        if success:
            p_last = current_path[-1].p
            p_spec = current_path[-2].p
            d = p_spec - p_last
            d_norm = norm(d)
            d /= d_norm
            ray = Ray2f(p_last, d, 1e-4, (1-1e-4)*d_norm)
            it = scene.ray_intersect(ray)
            if it.is_valid():
                success = False

        if success:
            solution_path = current_path
        else:
            solution_path = None
        return solution_path, intermediate_paths

    def draw(self, ctx, scene):
        super().draw(ctx, scene)
        s = scene.scale

        if self.animation_state > 1 and len(self.solution_paths) > 0:
            if len(self.solution_paths[0]) == 3:
                # Draw the "envelope of light paths manually"
                path_a = self.solution_paths[0]
                path_b = self.solution_paths[1]

                p1 = path_a[0].p
                p2 = path_b[1].p
                p3 = path_a[1].p
                p4 = path_a[2].p

                ctx.Save()

                ctx.FillColor(nvg.RGBA(80, 80, 80, 128))
                ctx.BeginPath()
                ctx.MoveTo(p1[0], p1[1])
                ctx.LineTo(p2[0], p2[1])
                ctx.LineTo(p3[0], p3[1])
                ctx.Fill()

                ctx.BeginPath()
                ctx.MoveTo(p4[0], p4[1])
                ctx.LineTo(p2[0], p2[1])
                ctx.LineTo(p3[0], p3[1])
                ctx.Fill()

                ctx.Restore()
            else:
                # Just draw the two extreme ends as seperate paths
                for path in self.solution_paths:
                    draw_path_lines(ctx, path, '', s)
        else:
            if self.solution_path:
                draw_path_lines(ctx, self.solution_path, '', s)



        for k, vtx in enumerate(self.seed_path):
            if vtx.shape.type == Shape.Type.Reflection or vtx.shape.type == Shape.Type.Refraction:

                if self.animation_state == 0:
                    draw_arrow(ctx, vtx.p, vtx.n, nvg.RGB(255, 0, 0), scale=s, length=0.25)
                elif self.animation_state > 0:
                    ctx.Save()
                    ctx.StrokeWidth(0.01*s)
                    ctx.FillColor(nvg.RGB(255, 0, 0))

                    normals = 0.33*self.normal_distr

                    M = normals.shape[0]
                    if M > 0:
                        n0 = vtx.s * normals[0, 0] + vtx.n * normals[0, 1]

                        ctx.BeginPath()
                        ctx.MoveTo(vtx.p[0] + n0[0], vtx.p[1] + n0[1])
                        for i in range(M-1):
                            n = vtx.s * normals[i+1, 0] + vtx.n * normals[i+1, 1]
                            ctx.LineTo(vtx.p[0] + n[0], vtx.p[1] + n[1])
                        ctx.LineTo(vtx.p[0] + n0[0], vtx.p[1] + n0[1])
                        ctx.Stroke()
                        ctx.Fill()

                    ctx.Restore()


        draw_dotted_path_lines(ctx, self.seed_path, s, spacing=0.02)


        scene.draw(ctx)

        # draw_path_normals(ctx, self.seed_path, scale=s)

        draw_path_vertices(ctx, self.seed_path, '', s)
        if self.animation_state <= 1:
            if self.solution_path:
                draw_path_vertices(ctx, self.solution_path, '', s)

        self.knob_start.draw(ctx)
        self.knob_end.draw(ctx)
        self.knob_spec.draw(ctx)

    def layout(self, window):
        strategy_tools = Widget(window)
        strategy_tools.set_layout(BoxLayout(Orientation.Horizontal,
                                            Alignment.Middle, 0, 3))
        Label(strategy_tools, "MNEE vs. SMS:")

        self.strategy_mnee_btn = Button(strategy_tools, "", icons.FA_CIRCLE)
        self.strategy_mnee_btn.set_flags(Button.Flags.RadioButton)
        self.strategy_mnee_btn.set_pushed(self.strategy_type == StrategyType.MNEE)
        def strategy_mnee_cb(state):
            if state:
                self.strategy_type = StrategyType.MNEE
        self.strategy_mnee_btn.set_change_callback(strategy_mnee_cb)

        self.strategy_sms_btn = Button(strategy_tools, "", icons.FA_CERTIFICATE)
        self.strategy_sms_btn.set_flags(Button.Flags.RadioButton)
        self.strategy_sms_btn.set_pushed(self.strategy_type == StrategyType.SMS)
        def strategy_sms_cb(state):
            if state:
                self.strategy_type = StrategyType.SMS
        self.strategy_sms_btn.set_change_callback(strategy_sms_cb)

        Label(strategy_tools, "  N=")
        self.n_bounces_box = IntBox(strategy_tools)
        self.n_bounces_box.set_fixed_size((50, 20))
        self.n_bounces_box.set_value(1)
        self.n_bounces_box.set_default_value("1")
        self.n_bounces_box.set_font_size(20)
        self.n_bounces_box.set_spinnable(True)
        self.n_bounces_box.set_min_value(1)
        self.n_bounces_box.set_value_increment(1)


        constraint_tools = Widget(window)
        constraint_tools.set_layout(BoxLayout(Orientation.Horizontal,
                                      Alignment.Middle, 0, 3))
        Label(constraint_tools, "Constraint type: ")

        self.constraint_hv_btn = Button(constraint_tools, "", icons.FA_RULER_COMBINED)
        self.constraint_hv_btn.set_flags(Button.Flags.RadioButton)
        self.constraint_hv_btn.set_pushed(self.constraint_type == ConstraintType.HalfVector)
        def constraint_hv_cb(state):
            if state:
                self.constraint_type = ConstraintType.HalfVector
        self.constraint_hv_btn.set_change_callback(constraint_hv_cb)

        self.constraint_dir_btn = Button(constraint_tools, "", icons.FA_DRAFTING_COMPASS)
        self.constraint_dir_btn.set_flags(Button.Flags.RadioButton)
        self.constraint_dir_btn.set_pushed(self.constraint_type == ConstraintType.AngleDifference)
        def constraint_dir_cb(state):
            if state:
                self.constraint_type = ConstraintType.AngleDifference
        self.constraint_dir_btn.set_change_callback(constraint_dir_cb)

        self.show_constraint_chb = CheckBox(constraint_tools, "Show")
        self.show_constraint_chb.set_checked(True)
        self.flip_constraint_chb = CheckBox(constraint_tools, "Flip")
        self.flip_constraint_chb.set_checked(False)

        steps_eps_tools = Widget(window)
        steps_eps_tools.set_layout(BoxLayout(Orientation.Horizontal,
                                             Alignment.Middle, 0, 3))

        Label(steps_eps_tools, "N")
        self.max_steps_sl = Slider(steps_eps_tools)
        max_steps_tb = TextBox(steps_eps_tools)
        max_steps_tb.set_value("20")
        max_steps_tb.set_font_size(20)
        max_steps_tb.set_alignment(TextBox.Alignment.Right)
        self.max_steps_sl.set_value(0.3878)
        def max_steps_cb(value):
            max_steps_tb.set_value("%i" % (1 + int(49*value)))
        self.max_steps_sl.set_callback(max_steps_cb)

        Label(steps_eps_tools, "eps")
        self.eps_sl = Slider(steps_eps_tools)
        eps_tb = TextBox(steps_eps_tools)
        eps_tb.set_value("1.0E-03")
        eps_tb.set_font_size(20)
        eps_tb.set_alignment(TextBox.Alignment.Right)
        self.eps_sl.set_value(0.285)
        def eps_cb(value):
            eps_tb.set_value("%.1E" % 10.0**(-(1 + value*7)))
        self.eps_sl.set_callback(eps_cb)

        roughness_tools = Widget(window)
        roughness_tools.set_layout(BoxLayout(Orientation.Horizontal,
                                             Alignment.Middle, 0, 3))
        Label(roughness_tools, "Roughness")
        self.roughness_sl = Slider(roughness_tools)
        self.roughness_sl.set_value(0.2)


        return [strategy_tools, constraint_tools, steps_eps_tools, roughness_tools], []

    def keyboard_event(self, key, scancode, action, modifiers):
        super().keyboard_event(key, scancode, action, modifiers)

        if key == glfw.KEY_RIGHT and action == glfw.PRESS:
            self.animating = not self.animating
            return True

        if key == glfw.KEY_UP and action == glfw.PRESS:
            self.animation_state += 1
            return True

        if key == glfw.KEY_DOWN and action == glfw.PRESS:
            if self.animation_state > 0:
                self.animation_state -= 1
            return True

    def max_steps(self):
        value = self.max_steps_sl.value()
        return 1 + int(49*value)

    def eps_threshold(self):
        value = self.eps_sl.value()
        return 10.0**(-(1 + value*7))
