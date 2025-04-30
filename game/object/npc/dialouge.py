import arcade
from core.constance import *


class Dialogue:
    def __init__(self, game, lines: list[str]):
        self.game = game
        self.lines = lines
        self.current_line_index = 0
        self.active = True
        self.font_size = 14
        self.padding = 20

        # Animation
        self.text_progress = 0  # How many letters are currently shown
        self.speed = 0.5  # Letters per frame (you can adjust)

    def on_update(self):
        if self.active:
            self.text_progress += self.speed

    def start(self, new_lines: list[str]):
        self.lines = new_lines
        self.current_line_index = 0
        self.text_progress = 0
        self.active = True

    def on_draw(self):

        if self.active:
            full_text = self.lines[self.current_line_index]

            # Calculate size
            text_lines = full_text.split("\n")
            max_line_length = max(len(line) for line in text_lines)
            width = max_line_length * (self.font_size // 2) + self.padding * 2
            height = len(text_lines) * (self.font_size + 5) + self.padding * 2
            y = 100
            x = SCREEN_WIDTH//2

            box = arcade.Rect(
                left=x - width // 2,
                bottom=y - height // 2,
                right=x + width // 2,
                top=y + height // 2,
            )

            arcade.draw_rect_filled(box, arcade.color.BLACK)

            # Draw the partial text
            partial_text = full_text[:int(self.text_progress)]
            arcade.draw_text(
                partial_text,
                SCREEN_WIDTH // 2,
                100,
                arcade.color.WHITE,
                font_size=self.font_size,
                anchor_x="center",
                anchor_y="center",
                align="center",
                width=width - self.padding * 2
            )

    def next_line(self):
        if self.text_progress < len(self.lines[self.current_line_index]):
            # If text is not finished showing, show it instantly
            self.text_progress = len(self.lines[self.current_line_index])
        else:
            # Move to next line
            self.current_line_index += 1
            self.text_progress = 0  # Reset animation

            if self.current_line_index >= len(self.lines):
                self.active = False
