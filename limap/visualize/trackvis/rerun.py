"""Module providing interactive visualization based on rerun."""
import os
import sys
from collections import defaultdict

import cv2
import rerun as rr
from scipy.spatial import transform

from .base import BaseTrackVisualizer

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vis_lines import rerun_get_line_segments
from vis_utils import test_point_inside_ranges


class RerunTrackVisualizer(BaseTrackVisualizer):
    def __init__(self, tracks):
        super(RerunTrackVisualizer, self).__init__(tracks)

    def vis_all_lines(self, n_visible_views=4, width=0.01, scale=1.0):
        rr.init("limap line visualization", spawn=True)
        self._log_lines_timeless(n_visible_views, width, scale)

    def vis_reconstruction(
        self,
        imagecols,
        n_visible_views=4,
        width=0.01,
        ranges=None,
        scale=1.0,
        cam_scale=1.0,
    ):
        rr.init("limap reconstruction visualization", spawn=True)
        rr.log_view_coordinates("world", up="+Z", timeless=True)

        # all lines (i.e., full reconstruction)
        self._log_lines_timeless(n_visible_views, width, scale, ranges)

        # sequential lines (i.e., as lines are reconstructed)
        self._log_lines_per_frame(n_visible_views, width, scale, ranges)

        # cameras and images
        self._log_camviews(imagecols.get_camviews(), ranges)

        # TODO scale for log_camviews

        # TODO remove cam_scale (?)

        # TODO optional sequence-mode logging (with lines appearing as images come in)
        # TODO visualize other data stored in output (keypoints, detected 2D lines)

        # TODO visualize line-point associationg (degree-1 point and degree-2 junctions)
        # TODO visualize parallel line association

    def _log_lines_timeless(self, n_visible_views, width=0.01, scale=1.0, ranges=None):
        lines = self.get_lines_n_visible_views(n_visible_views)
        line_segments = rerun_get_line_segments(lines, ranges=ranges, scale=scale)
        rr.log_line_segments(
            "world/lines",
            line_segments,
            stroke_width=width,
            color=[1.0, 0.0, 0.0],
            timeless=True,
        )

    def _log_lines_per_frame(self, n_visible_views, width=0.01, scale=1.0, ranges=None):
        """Log lines based on when they are visible in n_visible views."""
        for i, track in enumerate(self.tracks):
            if track.count_images() < n_visible_views:
                continue
            line_segments = rerun_get_line_segments(
                [track.line], ranges=ranges, scale=scale
            )
            if len(line_segments) == 0:
                continue
            frame_id = track.GetSortedImageIds()[n_visible_views - 1]
            rr.set_time_sequence("frame_id", frame_id)
            rr.log_line_segments(
                f"world/sequential_lines/#{i}",
                line_segments,
                stroke_width=width,
                color=[1.0, 0.0, 0.0],
            )

    def _log_camviews(self, camviews, ranges=None):
        for i, camview in enumerate(camviews):
            if ranges is not None:
                if not test_point_inside_ranges(camview.T(), ranges):
                    continue
            bgr_img = cv2.imread(camview.image_name())
            rgb_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)
            width, height = camview.w(), camview.h()
            rgb_img = cv2.resize(rgb_img, (width, height))
            rr.set_time_sequence("frame_id", i)
            rr.log_image("world/camera/image", rgb_img)
            translation_xyz = camview.T()
            quaternion_xyzw = transform.Rotation.from_matrix(camview.R()).as_quat()
            rr.log_rigid3(
                "world/camera",
                child_from_parent=(translation_xyz, quaternion_xyzw),
            )
            rr.log_view_coordinates("world/camera", xyz="RDF")
            rr.log_pinhole(
                "world/camera/image",
                child_from_parent=camview.K(),
                width=width,
                height=height,
            )