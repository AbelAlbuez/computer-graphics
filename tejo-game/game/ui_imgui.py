"""
Sistema de UI usando Dear ImGui para el juego de Tejo
Renderiza paneles con texto visible, barras de progreso y colores de equipo
"""

import imgui
from imgui.integrations.opengl import ProgrammablePipelineRenderer


class UISystemImGui:
    """
    Sistema de UI con Dear ImGui.
    Muestra información del juego en paneles superior e inferior.
    """
    
    def __init__(self, render_window, scene_mgr, camera):
        self.render_window = render_window
        self.scene_mgr = scene_mgr
        self.camera = camera
        self.imgui_renderer = None
        self.initialized = False
        
        self.power = 75
        self.angle = 45
        self.score_a = 0
        self.score_b = 0
        self.current_team = "A"
        self.tejos_remaining = 6
        
        self.launch_message = ""
        self.launch_message_timer = 0.0
    
    def initialize(self):
        """Inicializar ImGui y el renderer OpenGL"""
        print("\n" + "="*50)
        print("CONTROLES DEL JUEGO DE TEJO")
        print("="*50)
        print("W/S: Ajustar fuerza (50-100)")
        print("Flechas Arriba/Abajo: Ajustar angulo (20-70)")
        print("ESPACIO: Lanzar el tejo")
        print("R: Reiniciar juego")
        print("ESC: Salir")
        print("="*50 + "\n")
        
        try:
            imgui.create_context()
            self.imgui_renderer = ProgrammablePipelineRenderer()
            
            io = imgui.get_io()
            io.display_size = (
                self.render_window.getWidth(),
                self.render_window.getHeight()
            )
            
            self._setup_style()
            self.initialized = True
            print("ImGui inicializado correctamente")
            
        except Exception as e:
            print(f"Error inicializando ImGui: {e}")
            self.initialized = False
    
    def _setup_style(self):
        """Configurar estilo visual de ImGui"""
        style = imgui.get_style()
        style.window_rounding = 0.0
        style.frame_rounding = 4.0
        style.window_border_size = 0.0
        style.frame_border_size = 1.0
        style.item_spacing = (10, 8)
        style.window_padding = (15, 15)
        
        colors = style.colors
        colors[imgui.COLOR_WINDOW_BACKGROUND] = (0.1, 0.1, 0.12, 0.95)
        colors[imgui.COLOR_TEXT] = (1.0, 1.0, 1.0, 1.0)
        colors[imgui.COLOR_FRAME_BACKGROUND] = (0.2, 0.2, 0.22, 1.0)
        colors[imgui.COLOR_FRAME_BACKGROUND_HOVERED] = (0.3, 0.3, 0.32, 1.0)
        colors[imgui.COLOR_FRAME_BACKGROUND_ACTIVE] = (0.35, 0.35, 0.37, 1.0)
        colors[imgui.COLOR_BORDER] = (0.4, 0.4, 0.45, 0.5)
    
    def new_frame(self):
        """Iniciar nuevo frame de ImGui"""
        if not self.initialized:
            return
        
        try:
            io = imgui.get_io()
            io.display_size = (
                self.render_window.getWidth(),
                self.render_window.getHeight()
            )
            imgui.new_frame()
        except Exception as e:
            print(f"Error en new_frame: {e}")
    
    def render(self):
        """Renderizar toda la UI"""
        if not self.initialized:
            return
        
        try:
            window_width = self.render_window.getWidth()
            window_height = self.render_window.getHeight()
            
            self._render_top_panel(window_width)
            self._render_bottom_panel(window_width, window_height)
            
            if self.launch_message_timer > 0:
                self._render_launch_message(window_width, window_height)
            
        except Exception as e:
            print(f"Error en render: {e}")
    
    def end_frame(self):
        """Finalizar frame y renderizar"""
        if not self.initialized:
            return
        
        try:
            imgui.render()
            self.imgui_renderer.render(imgui.get_draw_data())
        except Exception as e:
            print(f"Error en end_frame: {e}")
    
    def _render_top_panel(self, window_width):
        """Renderizar panel superior con scores y turno"""
        panel_height = 80
        
        imgui.set_next_window_position(0, 0)
        imgui.set_next_window_size(window_width, panel_height)
        
        flags = (
            imgui.WINDOW_NO_TITLE_BAR |
            imgui.WINDOW_NO_RESIZE |
            imgui.WINDOW_NO_MOVE |
            imgui.WINDOW_NO_SCROLLBAR |
            imgui.WINDOW_NO_COLLAPSE
        )
        
        imgui.begin("TopPanel", flags=flags)
        
        column_width = window_width / 3
        
        imgui.columns(3, "top_columns", False)
        imgui.set_column_width(0, column_width)
        imgui.set_column_width(1, column_width)
        imgui.set_column_width(2, column_width)
        
        # Equipo A (Rojo)
        imgui.text_colored("EQUIPO A", 1.0, 0.3, 0.3, 1.0)
        imgui.text("(Rojo)")
        imgui.spacing()
        imgui.text_colored(f"Puntos: {self.score_a}", 1.0, 0.5, 0.5, 1.0)
        
        imgui.next_column()
        
        # Turno actual (Centro)
        imgui.text("TURNO ACTUAL")
        imgui.spacing()
        
        if self.current_team == "A":
            imgui.text_colored(f"EQUIPO {self.current_team}", 1.0, 0.3, 0.3, 1.0)
        else:
            imgui.text_colored(f"EQUIPO {self.current_team}", 0.3, 1.0, 0.3, 1.0)
        
        imgui.text(f"Tejos restantes: {self.tejos_remaining}")
        
        imgui.next_column()
        
        # Equipo B (Verde)
        imgui.text_colored("EQUIPO B", 0.3, 1.0, 0.3, 1.0)
        imgui.text("(Verde)")
        imgui.spacing()
        imgui.text_colored(f"Puntos: {self.score_b}", 0.5, 1.0, 0.5, 1.0)
        
        imgui.columns(1)
        imgui.end()
    
    def _render_bottom_panel(self, window_width, window_height):
        """Renderizar panel inferior con fuerza, controles y angulo"""
        panel_height = 100
        
        imgui.set_next_window_position(0, window_height - panel_height)
        imgui.set_next_window_size(window_width, panel_height)
        
        flags = (
            imgui.WINDOW_NO_TITLE_BAR |
            imgui.WINDOW_NO_RESIZE |
            imgui.WINDOW_NO_MOVE |
            imgui.WINDOW_NO_SCROLLBAR |
            imgui.WINDOW_NO_COLLAPSE
        )
        
        imgui.begin("BottomPanel", flags=flags)
        
        column_width = window_width / 3
        
        imgui.columns(3, "bottom_columns", False)
        imgui.set_column_width(0, column_width)
        imgui.set_column_width(1, column_width)
        imgui.set_column_width(2, column_width)
        
        # Fuerza (Izquierda)
        imgui.text_colored("FUERZA", 1.0, 0.7, 0.2, 1.0)
        imgui.spacing()
        
        power_normalized = (self.power - 50) / 50.0
        imgui.push_style_color(imgui.COLOR_PLOT_HISTOGRAM, 1.0, 0.6, 0.1, 1.0)
        imgui.progress_bar(power_normalized, (column_width - 40, 25), f"{int(self.power)}%")
        imgui.pop_style_color()
        
        imgui.text("W/S para ajustar")
        
        imgui.next_column()
        
        # Controles (Centro)
        imgui.text_colored("CONTROLES", 0.8, 0.8, 0.8, 1.0)
        imgui.spacing()
        imgui.text("ESPACIO = Lanzar")
        imgui.text("R = Reiniciar")
        imgui.text("ESC = Salir")
        
        imgui.next_column()
        
        # Angulo (Derecha)
        imgui.text_colored("ANGULO", 0.2, 0.7, 1.0, 1.0)
        imgui.spacing()
        
        angle_normalized = (self.angle - 20) / 50.0
        imgui.push_style_color(imgui.COLOR_PLOT_HISTOGRAM, 0.2, 0.6, 1.0, 1.0)
        imgui.progress_bar(angle_normalized, (column_width - 40, 25), f"{int(self.angle)} grados")
        imgui.pop_style_color()
        
        imgui.text("Flechas para ajustar")
        
        imgui.columns(1)
        imgui.end()
    
    def _render_launch_message(self, window_width, window_height):
        """Renderizar mensaje de lanzamiento en el centro"""
        msg_width = 300
        msg_height = 60
        
        imgui.set_next_window_position(
            (window_width - msg_width) / 2,
            (window_height - msg_height) / 2
        )
        imgui.set_next_window_size(msg_width, msg_height)
        
        flags = (
            imgui.WINDOW_NO_TITLE_BAR |
            imgui.WINDOW_NO_RESIZE |
            imgui.WINDOW_NO_MOVE |
            imgui.WINDOW_NO_SCROLLBAR |
            imgui.WINDOW_NO_COLLAPSE
        )
        
        imgui.begin("LaunchMessage", flags=flags)
        imgui.text_colored(self.launch_message, 1.0, 1.0, 0.3, 1.0)
        imgui.end()
    
    def update_team_display(self, team_name, team_number, tejos_remaining):
        """Actualizar visualizacion del equipo actual"""
        self.current_team = team_name
        self.tejos_remaining = tejos_remaining
        print(f"\n>>> TURNO: EQUIPO {team_name} - Quedan {tejos_remaining} tejos")
    
    def update_score_display(self, score_a, score_b):
        """Actualizar puntajes"""
        self.score_a = score_a
        self.score_b = score_b
        print(f"MARCADOR - Equipo A: {score_a} | Equipo B: {score_b}")
    
    def show_launch_info(self, power, angle):
        """Mostrar informacion del lanzamiento"""
        self.power = power
        self.angle = angle
        self.launch_message = f"LANZADO! F:{power}% A:{angle} grados"
        self.launch_message_timer = 2.0
        print(f"\nLANZADO! Fuerza: {power}% | Angulo: {angle} grados")
        print("-" * 40)
    
    def show_score_info(self, breakdown, team_scores, current_team):
        """Mostrar informacion de puntuacion"""
        print("RESULTADO:")
        for detail in breakdown['details']:
            print(f"  - {detail}")
        
        if breakdown['final_total'] > 0:
            print(f"  - Puntos: {breakdown['final_total']}")
        else:
            print(f"  - Sin puntos")
        print("-" * 40)
    
    def update_power(self, power):
        """Actualizar valor de fuerza"""
        self.power = power
        self._print_status()
    
    def update_angle(self, angle):
        """Actualizar valor de angulo"""
        self.angle = angle
        self._print_status()
    
    def update(self, power, angle):
        """Actualizar fuerza y angulo"""
        self.power = power
        self.angle = angle
    
    def _print_status(self):
        """Imprimir estado en consola"""
        print(f"\rFuerza: {int(self.power):3d}% | Angulo: {int(self.angle):2d} grados  ", end="", flush=True)
    
    def frame_update(self, delta_time):
        """Actualizacion por frame"""
        if self.launch_message_timer > 0:
            self.launch_message_timer -= delta_time
            if self.launch_message_timer <= 0:
                self.launch_message = ""
    
    def cleanup(self):
        """Limpiar recursos"""
        if self.imgui_renderer:
            self.imgui_renderer.shutdown()
        print("\nImGui limpiado correctamente")
