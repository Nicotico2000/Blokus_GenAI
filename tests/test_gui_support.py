from pathlib import Path
import unittest

from blokus.gui_support import (
    build_board_metrics,
    board_cell_from_point,
    format_suggestion_label,
    load_sidebar_piece_slots,
    piece_panel_layout,
    transformed_cell_map,
)
from blokus.pieces import PIECE_IDS


class GuiSupportTests(unittest.TestCase):
    def test_board_cell_mapping_detects_top_left_cell(self) -> None:
        metrics = build_board_metrics(338, 66, 820)
        cell = board_cell_from_point(metrics.grid_origin_x + 5, metrics.grid_origin_y + 5, metrics)
        self.assertEqual(cell, (0, 0))

    def test_board_cell_mapping_rejects_outside_points(self) -> None:
        metrics = build_board_metrics(338, 66, 820)
        self.assertIsNone(board_cell_from_point(0, 0, metrics))

    def test_transformed_cell_map_preserves_piece_cardinality(self) -> None:
        mapping = transformed_cell_map("F5", rotation=1, flipped=True)
        self.assertEqual(len(mapping), 5)
        self.assertEqual(len(set(mapping.values())), 5)

    def test_piece_panel_layout_returns_all_piece_positions(self) -> None:
        positions = piece_panel_layout(PIECE_IDS, panel_left=1190, panel_top=320, panel_width=220)
        self.assertEqual(set(positions), set(PIECE_IDS))

    def test_sidebar_piece_slots_cover_all_phase_one_pieces(self) -> None:
        slots = load_sidebar_piece_slots(
            Path("Brokus Graphics/SideBars.svg"),
            window_width=1500,
            window_height=950,
        )
        self.assertEqual(set(slots), set(PIECE_IDS))
        self.assertTrue(all(slot.bbox[2] > slot.bbox[0] for slot in slots.values()))

    def test_suggestion_label_is_human_readable(self) -> None:
        label = format_suggestion_label("L5", 3, 4, 2, True)
        self.assertIn("L5", label)
        self.assertIn("(3, 4)", label)
        self.assertIn("rot=2", label)
        self.assertIn("flip", label)


if __name__ == "__main__":
    unittest.main()
