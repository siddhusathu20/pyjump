# PyJump (class 12 project)
# by Siddharth Jai Gokulan

import arcade
import arcade.gui
import arcade.gui.widgets
import arcade.gui.widgets.layout
import arcade.gui.widgets.text

LEVEL_TIPS = {
    1: """Press SPACE to jump.
Your progress will be saved
after clearing a level.""",
    2: """NEW SKILL: Double Jump
Press SPACE while in midair
after jumping to jump again.""",
    3: """NEW SKILL: Reverse Polarity
Hold BACKSPACE to
reverse your
polarity.""",
    4: """ZERO GRAVITY:
Press SPACE to change
your vertical movement
direction.""",
    5: """BULLET TIME:
Press ENTER to enter
bullet time and press
it again to exit
bullet time."""
}


class Menu(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.title_text = arcade.Text("PyJump", self.window.width*0.5, self.window.height*0.7, arcade.csscolor.WHITE,
                                      font_name="Bahnschrift" , font_size = 48, anchor_x="center", bold=True)
        self.play_button = arcade.gui.UIFlatButton(text="PLAY", width=250)
        self.button_anchor = self.manager.add(arcade.gui.UIAnchorLayout())
        self.button_anchor.add(child=self.play_button)
        @self.play_button.event("on_click")
        def start_game(event):
            game = Game()
            game.setup()
            self.window.show_view(game)
    
    def on_show_view(self):
        self.window.background_color = arcade.csscolor.DARK_BLUE
        self.manager.enable()
        self.window.default_camera.use()
    
    def on_hide_view(self):
        self.manager.disable()
    
    def on_draw(self):
        self.clear()
        self.manager.draw()
        self.title_text.draw()
    
    def on_resize(self, width: int, height: int):
        self.window.show_view(Menu())


class Win(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.title_text = arcade.Text("Thanks for playing!", self.window.width*0.5, self.window.height*0.7, arcade.csscolor.WHITE,
                                      font_name="Bahnschrift" , font_size = 48, anchor_x="center", bold=True)
        self.play_button = arcade.gui.UIFlatButton(text="START OVER", width=250)
        self.button_anchor = self.manager.add(arcade.gui.UIAnchorLayout())
        self.button_anchor.add(child=self.play_button)
        @self.play_button.event("on_click")
        def start_game(event):
            with open("save1.txt", "w+") as self.save1:
                self.save1.write("1")
            game = Game()
            game.setup()
            self.window.show_view(game)
    
    def on_show_view(self):
        self.window.background_color = arcade.csscolor.GREEN
        self.manager.enable()
        self.window.default_camera.use()
    
    def on_hide_view(self):
        self.manager.disable()
    
    def on_draw(self):
        self.clear()
        self.manager.draw()
        self.title_text.draw()
    
    def on_resize(self, width: int, height: int):
        self.window.show_view(Win())


class Game(arcade.View):
    def __init__(self):
        super().__init__()
        self.cube_texture = None
        self.cube_sprite = None
        self.camera = None
        self.tiled_map = None
        self.attempt = 1
        self.attempt_text = None
        self.anti_grav = False
        self.zero_grav = False
        self.grav_const = self.window.height/480
        self.reverse = False
        self.can_double_jump = False
        self.can_reverse = False
        self.can_use_bullet_time = False
        self.in_bullet_time = False
        self.x_speed = 4
        self.y_speed = 10
        try:
            with open("save1.txt", "r+") as self.save1:
                self.save1.seek(0)
                self.level = int(self.save1.read())
        except:
            with open("save1.txt", "w+") as self.save1:
                self.save1.write("1")
            with open("save1.txt", "r+") as self.save1:
                self.save1.seek(0)
                self.level = int(self.save1.read())
    
    def setup(self):
        self.window.background_color = arcade.csscolor.SKY_BLUE
        self.cube_texture = arcade.load_texture("assets/sphere.png")
        self.cube_sprite = arcade.Sprite(self.cube_texture, 0.03*(self.window.height/480))
        self.cube_sprite.position = [50*(self.window.height/480), 70*(self.window.height/480)]
        tile_layer_options = {
            "Platforms": {"use_spatial_hash": True}
        }
        self.tiled_map = arcade.load_tilemap(f"assets/map{self.level}.json", scaling=self.window.height/480, layer_options=tile_layer_options)
        self.scene = arcade.Scene.from_tilemap(self.tiled_map)
        self.camera = arcade.camera.Camera2D()
        self.attempt_text = arcade.Text(f"LEVEL {self.level}, ATTEMPT {self.attempt}", color=arcade.csscolor.BLACK,
                                        x = 100*(self.window.height/480), y = 400*(self.window.height/480), font_size = 20, bold = True)
        self.tip_text = arcade.Text(LEVEL_TIPS[self.level], multiline=True, width=400, color=arcade.csscolor.BLACK,
                                    x = 100*(self.window.height/480), y = 350*(self.window.height/480), font_size = 20, bold = False)
        self.grav_const = self.window.height/480
        self.abin_sir = arcade.PhysicsEnginePlatformer(self.cube_sprite, walls=self.scene["Platforms"], gravity_constant=self.grav_const)
        self.anti_grav = False
        self.zero_grav = False
        self.reverse = False
        self.in_bullet_time = False
        self.x_speed = 4
        self.y_speed = 10
        if self.level >= 2:
            self.can_double_jump = True
        if self.level >= 3:
            self.can_reverse = True
        if self.level >= 5:
            self.can_use_bullet_time = True
        if self.can_double_jump is True:
            self.abin_sir.enable_multi_jump(2)
        

    def on_draw(self):
        self.clear()
        self.camera.use()
        self.scene.draw()
        self.cube_sprite.draw()
        self.attempt_text.draw()
        self.tip_text.draw()

    def on_update(self, delta_time):
        print(arcade.get_fps())
        if self.reverse is True:
            self.cube_sprite.change_x = -self.x_speed*(self.window.height/480)
        else:
            self.cube_sprite.change_x = self.x_speed*(self.window.height/480)
        if (self.anti_grav is True and self.reverse is False) or (self.anti_grav is False and self.reverse is True):
            if self.in_bullet_time is True:
                self.cube_sprite.change_angle = -2.5
            else:
                self.cube_sprite.change_angle = -5
        elif (self.anti_grav is False and self.reverse is False) or (self.anti_grav is True and self.reverse is True):
            if self.in_bullet_time is True:
                self.cube_sprite.change_angle = 2.5
            else:
                self.cube_sprite.change_angle = 5
        self.camera.position = [self.cube_sprite.center_x+100, 240*(self.window.height/480)]
        self.abin_sir.update()
        anti_grav_block = arcade.check_for_collision_with_list(self.cube_sprite, self.scene["Anti Grav"])
        for block in anti_grav_block:
            block.remove_from_sprite_lists()
            self.anti_grav = not self.anti_grav
            self.grav_const = -self.grav_const
            self.abin_sir = arcade.PhysicsEnginePlatformer(self.cube_sprite, walls = self.scene["Platforms"], gravity_constant = self.grav_const)
            if self.can_double_jump is True:
                self.abin_sir.enable_multi_jump(2)
        zero_grav_block = arcade.check_for_collision_with_list(self.cube_sprite, self.scene["Zero Grav"])
        for block in zero_grav_block:
            block.remove_from_sprite_lists()
            self.zero_grav = not self.zero_grav
            if self.grav_const == 0:
                if self.anti_grav is True:
                    self.grav_const = -1*(self.window.height/480)
                else:
                    self.grav_const = self.window.height/480
            else:
                self.grav_const = 0
                self.cube_sprite.change_y = (self.y_speed/1.5)*(self.window.height/480)
            self.abin_sir = arcade.PhysicsEnginePlatformer(self.cube_sprite, walls = self.scene["Platforms"], gravity_constant = self.grav_const)
            if self.can_double_jump is True:
                self.abin_sir.enable_multi_jump(2)
        if arcade.check_for_collision_with_list(self.cube_sprite, self.scene["Avoid"]):
            self.attempt += 1
            self.setup()
        if arcade.check_for_collision_with_list(self.cube_sprite, self.scene["Finish"]):
            if self.level < 5:
                self.level += 1
                with open("save1.txt", "r+") as self.save1:
                    self.save1.seek(0)
                    self.save1.write(f"{self.level}")
                    self.save1.truncate()
                    self.save1.seek(0)
                self.attempt = 1
                self.setup()
            else:
                self.window.show_view(Win())
    
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER and self.can_use_bullet_time is True:
            if self.in_bullet_time is False:
                self.x_speed /= 2
                self.y_speed /= 2
                self.grav_const /= 4
                self.abin_sir = arcade.PhysicsEnginePlatformer(self.cube_sprite, walls = self.scene["Platforms"], gravity_constant = self.grav_const)
                if self.can_double_jump is True:
                    self.abin_sir.enable_multi_jump(2)
            elif self.in_bullet_time is True:
                self.x_speed *= 2
                self.y_speed *= 2
                self.grav_const *= 4
                self.abin_sir = arcade.PhysicsEnginePlatformer(self.cube_sprite, walls = self.scene["Platforms"], gravity_constant = self.grav_const)
                if self.can_double_jump is True:
                    self.abin_sir.enable_multi_jump(2)
            self.in_bullet_time = not self.in_bullet_time
        if key == arcade.key.BACKSPACE and self.can_reverse is True:
            self.reverse = True
        if key == arcade.key.SPACE:
            if self.zero_grav is False:
                if self.anti_grav is False:
                    if self.abin_sir.can_jump(5):
                        self.abin_sir.increment_jump_counter()
                        self.cube_sprite.change_y = self.y_speed*(self.window.height/480)
                else:
                    if self.abin_sir.can_jump(-5):
                        self.abin_sir.increment_jump_counter()
                        self.cube_sprite.change_y = -self.y_speed*(self.window.height/480)
            else:
                if self.cube_sprite.change_y != 0:
                    self.cube_sprite.change_y = -self.cube_sprite.change_y
                else:
                    if self.abin_sir.can_jump(5):
                        self.cube_sprite.change_y = self.y_speed/1.5
                    elif self.abin_sir.can_jump(-5):
                        self.cube_sprite.change_y = -self.y_speed/1.5
        if key == arcade.key.R:
            self.setup()
        if key == arcade.key.ESCAPE:
            self.window.show_view(Menu())
        
    def on_key_release(self, key, modifiers):
        if key == arcade.key.SPACE and self.zero_grav is False:
            self.cube_sprite.change_y = 0
        if key == arcade.key.BACKSPACE and self.level >= 3:
            self.reverse = False
    
    def on_resize(self, width: int, height: int):
        self.window.show_view(Menu())
    

if __name__ == "__main__":
    arcade.enable_timings()
    game_window = arcade.Window(640, 480, "PyJump", resizable=True)
    menu = Menu()
    game_window.show_view(menu)
    arcade.run()