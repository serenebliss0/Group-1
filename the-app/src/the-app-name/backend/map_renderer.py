"""Draw the explorable map: PNG asset or procedural fallback."""

from pathlib import Path

from .theme import (
    ASH,
    BG,
    BUILDING,
    DIM,
    EMBER,
    MAP_HEIGHT,
    MAP_WIDTH,
    MUTED_GREEN,
    ROAD,
    TOXIC,
    TRASH,
    WATER_TOXIC,
)
from .world import OBSTACLES

ASSETS = Path(__file__).resolve().parent.parent / "assets" / "images"


class MapRenderer:
    """Renders base map layers onto a Tk canvas; keeps PhotoImage reference alive."""

    def __init__(self):
        self._photo = None

    def draw_base(self, canvas, layer_ids: dict) -> bool:
        """Return True if a PNG map was drawn."""
        layer_ids.clear()
        drawn_image = self._draw_png_map(canvas)
        if drawn_image:
            self._draw_map_markers(canvas, layer_ids, on_image=True)
            return True
        self._draw_procedural_map(canvas, layer_ids)
        return False

    def _draw_png_map(self, canvas) -> bool:
        try:
            from PIL import Image, ImageTk
        except ImportError:
            return False

        path = ASSETS / "game_map.png"
        if not path.exists():
            return False
        try:
            raw = Image.open(path).convert("RGB")
            if raw.size != (MAP_WIDTH, MAP_HEIGHT):
                raw = raw.resize((MAP_WIDTH, MAP_HEIGHT), Image.LANCZOS)
            self._photo = ImageTk.PhotoImage(raw)
            canvas.create_image(0, 0, image=self._photo, anchor="nw", tags=("map_bg",))
            return True
        except OSError:
            return False

    def _draw_procedural_map(self, canvas, layer_ids: dict):
        c = canvas
        c.create_rectangle(0, 0, MAP_WIDTH, MAP_HEIGHT, fill="#14100c", outline="", tags=("map_bg",))

        # Fog / districts
        for fx, fy, fw, fh in (
            (0, 0, MAP_WIDTH, 400),
            (0, 1800, MAP_WIDTH, 800),
            (0, 0, 350, MAP_HEIGHT),
            (2250, 0, 350, MAP_HEIGHT),
        ):
            c.create_rectangle(fx, fy, fx + fw, fy + fh, fill="#18120e", outline="", tags=("map_bg",))

        # Roads
        for y in range(200, MAP_HEIGHT, 400):
            c.create_rectangle(80, y, MAP_WIDTH - 80, y + 48, fill=ROAD, outline="", tags=("road",))
        for x in range(200, MAP_WIDTH, 450):
            c.create_rectangle(x, 80, x + 40, MAP_HEIGHT - 80, fill=ROAD, outline="", tags=("road",))

        # Central plaza
        c.create_oval(1100, 1100, 1500, 1500, fill="#1c1610", outline=DIM, tags=("map_bg",))

        layer_ids["river"] = c.create_rectangle(
            1050, 880, 1350, 1020, fill=WATER_TOXIC, outline=DIM, width=1, tags=("river",)
        )
        layer_ids["pipe_leak"] = c.create_oval(
            670, 530, 750, 590, fill=TOXIC, outline=EMBER, tags=("pipe_leak",)
        )
        layer_ids["tree"] = c.create_polygon(
            1600, 1280, 1580, 1340, 1620, 1340, fill=ASH, outline=DIM, tags=("tree",)
        )
        c.create_rectangle(1590, 1340, 1610, 1375, fill=DIM, tags=("tree",))

        layer_ids["purifier"] = c.create_rectangle(
            1900, 600, 2020, 700, fill=BUILDING, outline=ASH, tags=("purifier",)
        )
        layer_ids["garbage"] = c.create_rectangle(
            800, 1760, 960, 1880, fill=TRASH, outline=DIM, tags=("garbage",)
        )
        layer_ids["factory"] = c.create_rectangle(
            200, 1600, 450, 1850, fill="#1a1410", outline=ASH, width=2, tags=("factory",)
        )
        c.create_text(325, 1720, text="FACTORY", fill=DIM, font=("Courier", 9), tags=("factory",))

        layer_ids["billboard"] = c.create_rectangle(
            2150, 450, 2350, 580, fill="#2a1e12", outline=EMBER, tags=("billboard",)
        )
        c.create_text(2250, 510, text="BREATHE", fill="#3a2a18", font=("Courier", 11, "bold"), tags=("billboard",))

        for lx in (2270, 2295, 2320):
            layer_ids.setdefault("streetlights", []).append(
                c.create_rectangle(lx, 1360, lx + 12, 1500, fill=DIM, tags=("streetlights",))
            )

        for obs in OBSTACLES:
            c.create_rectangle(
                obs["x"], obs["y"], obs["x"] + obs["w"], obs["y"] + obs["h"],
                fill=BUILDING, outline=ASH, width=1, tags=("obstacle",),
            )

        c.create_rectangle(1040, 360, 1090, 450, fill="#3a2818", outline=EMBER, tags=("sign",))
        c.create_text(1065, 400, text="!", fill=EMBER, font=("Courier", 14, "bold"), tags=("sign",))

        c.create_text(
            1300, 200, text="SECTOR 7 — ABANDONED", fill=DIM, font=("Courier", 12), tags=("deco",),
        )
        c.create_text(
            400, 400, text="nothing remained\nuntil something did",
            fill="#2a2218", font=("Courier", 9, "italic"), tags=("deco",),
        )
        c.create_oval(1240, 1240, 1360, 1360, outline=DIM, dash=(6, 4), tags=("memorial",))
        c.create_text(1300, 1300, text="?", fill="#6b5a48", font=("Courier", 16), tags=("memorial",))

    def _draw_map_markers(self, canvas, layer_ids: dict, on_image: bool):
        """Overlay key zones when using PNG so state changes can tint regions."""
        if not on_image:
            return
        layer_ids["river"] = canvas.create_rectangle(
            1050, 880, 1350, 1020, fill="", outline=WATER_TOXIC, width=2, tags=("river",)
        )
        layer_ids["pipe_leak"] = canvas.create_oval(
            670, 530, 750, 590, fill="", outline=TOXIC, width=2, tags=("pipe_leak",)
        )
