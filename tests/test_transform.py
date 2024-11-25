from unittest.mock import patch

import numpy as np
import pytest

from mplbasketball.utils import transform


@patch("mplbasketball.utils._get_court_params_in_desired_units")
def test_transform_same_orientation(mock_get_court_params):
    # Mock court parameters for NBA court
    mock_get_court_params.return_value = {"court_dims": [94.0, 50.0]}

    x = np.array([10, 20, 30])
    y = np.array([15, 25, 35])

    # Test for NBA court with no orientation change
    transformed_x, transformed_y = transform(x, y, fr="h", to="h", origin="center", court_type="nba")
    np.testing.assert_array_equal(transformed_x, x)
    np.testing.assert_array_equal(transformed_y, y)


@patch("mplbasketball.utils._get_court_params_in_desired_units")
def test_transform_horizontal_to_vertical(mock_get_court_params):
    mock_get_court_params.return_value = {"court_dims": [94.0, 50.0]}

    x = np.array([10, 20, 30])
    y = np.array([15, 25, 35])

    # Test horizontal to vertical transformation
    transformed_x, transformed_y = transform(x, y, fr="h", to="v", origin="center", court_type="wnba")
    expected_x = -y
    expected_y = x
    np.testing.assert_array_equal(transformed_x, expected_x)
    np.testing.assert_array_equal(transformed_y, expected_y)


@patch("mplbasketball.utils._get_court_params_in_desired_units")
def test_transform_with_origin_top_left(mock_get_court_params):
    mock_get_court_params.return_value = {"court_dims": [94.0, 50.0]}

    x = np.array([10, 20, 30])
    y = np.array([15, 25, 35])

    # Test transformation with origin at top-left
    transformed_x, transformed_y = transform(x, y, fr="h", to="h", origin="top-left", court_type="ncaa")
    np.testing.assert_array_equal(transformed_x, x)
    np.testing.assert_array_equal(transformed_y, y)


@patch("mplbasketball.utils._get_court_params_in_desired_units")
def test_invalid_orientation(mock_get_court_params):
    mock_get_court_params.return_value = {"court_dims": [94.0, 50.0]}

    x = np.array([10, 20, 30])
    y = np.array([15, 25, 35])

    # Test invalid orientation
    with pytest.raises(ValueError):
        transform(x, y, fr="invalid", to="h", origin="center", court_type="nba")


@patch("mplbasketball.utils._get_court_params_in_desired_units")
def test_invalid_court_type(mock_get_court_params):
    mock_get_court_params.return_value = {"court_dims": [94.0, 50.0]}

    x = np.array([10, 20, 30])
    y = np.array([15, 25, 35])

    # Test invalid court type
    with pytest.raises(ValueError):
        transform(x, y, fr="h", to="h", origin="center", court_type="invalid")
