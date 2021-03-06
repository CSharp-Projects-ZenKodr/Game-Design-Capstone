""" Module for handling data requests from the client. """

from flask_socketio import emit

from global_context import CITIES, RESOURCE_NODES
from utils import get_logger
from world.coordinates import Coordinate
from server import login_required, socketio, current_user

LOGGER = get_logger(__name__)


@socketio.on("get_cities")
@login_required
def get_cities(message):  # pylint: disable=unused-argument
    """ Trigger a 'load_city' event for each city in the game. """
    LOGGER.debug(f"City list requested by {current_user}")
    for city in CITIES.values():
        emit("load_city", city)


@socketio.on("get_city_data")
@login_required
def get_city_data(message):
    """ Send the data for a city to the requesting player. """
    position = message["position"]

    city = CITIES.get(Coordinate.load(position))
    LOGGER.debug(f"{current_user} loading city {city}")
    if city:
        emit("update_city", city)


@socketio.on("get_resource_data")
@login_required
def get_resource_data(message):  # pylint: disable=unused-argument
    """ Send the position of all resource nodes to a player. """
    LOGGER.debug(f"Resource nodes requested by {current_user}")
    for position, resource in RESOURCE_NODES.items():
        emit("load_resource", {"position": position, "type": resource.name})
