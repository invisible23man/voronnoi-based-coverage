import pytest
from scipy.spatial import Voronoi
from voronoi import voronoi_finite_polygons_2d

def test_voronoi_finite_polygons_2d():
    points = [[0, 0], [1, 0], [0, 1], [1, 1]]
    vor = Voronoi(points)
    radius = 1
    regions, vertices = voronoi_finite_polygons_2d(vor, radius)

    assert len(regions) == len(points)
    assert len(vertices) == len(vor.vertices)
