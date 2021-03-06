"""The NetRadio Media Source integration."""
import asyncio
from homeassistant.components.media_player import ATTR_MEDIA_CONTENT_ID
import logging
import voluptuous as vol

from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.config_validation import string, url

from .media_source import NetRadioSource

from .const import (
    MIME_TYPE,
    DOMAIN,
    ENTITY_ID,
    CONF_NETRADIO_RADIOS,
    CONF_NETRADIO_RADIO_URL,
    CONF_NETRADIO_RADIO_NAME,
    CONF_NETRADIO_RADIO_ICON,
)

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_NETRADIO_RADIOS): vol.All(
                    cv.ensure_list,
                    [
                        {
                            vol.Required(CONF_NETRADIO_RADIO_URL): cv.url,
                            vol.Required(CONF_NETRADIO_RADIO_NAME): str,
                            vol.Optional(CONF_NETRADIO_RADIO_ICON): cv.url,
                        }
                    ],
                )
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

ATTR_PLAYER_ENTITY = "entity_id"
ATTR_IDX = "radio_index"

SERVICE_START_RADIO = "start_radio"

SERVICE_START_RADIO_SCHEMA = vol.Schema(
    {
        vol.Required(ATTR_IDX): cv.positive_int,
        vol.Required(ATTR_PLAYER_ENTITY): cv.entity_id,
    }
)

SERVICE_NEXT_RADIO = "next_radio"
SERVICE_PREV_RADIO = "prev_radio"

SERVICE_NEXT_RADIO_SCHEMA = vol.Schema(
    {
        vol.Required(ATTR_PLAYER_ENTITY): cv.entity_id,
    }
)


_LOGGER = logging.getLogger(__name__)

# TODO List the platforms that you want to support.
# For your initial PR, limit it to 1 platform.
PLATFORMS = ["media_source"]


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the NetRadio Media Source component."""

    def start_radio(service):
        """Start radio on specified player entity."""
        idx = service.data[ATTR_IDX]
        player = service.data.get(ATTR_PLAYER_ENTITY)
        radios = config[DOMAIN][CONF_NETRADIO_RADIOS]

        if idx < len(radios):
            # entity_id: media_player.bang_olufsen media_content_id: http://streams.greenhost.nl:8080/jazz media_content_type: music
            hass.services.call(
                "media_player",
                "play_media",
                {
                    "entity_id": player,
                    "media_content_id": radios[idx].get(CONF_NETRADIO_RADIO_URL),
                    "media_content_type": MIME_TYPE,
                },
                False,
            )

    def next_radio(service):
        """Switch Radio to the next entity."""
        player = service.data.get(ATTR_PLAYER_ENTITY)
        radios = config[DOMAIN][CONF_NETRADIO_RADIOS]
        url: string = hass.states.get(player).attributes.get(ATTR_MEDIA_CONTENT_ID)
        idx: int = 0
        for i in radios:
            if i.get(CONF_NETRADIO_RADIO_URL) == url:
                idx = radios.index(i)
        idx = idx + 1
        if idx >= len(radios):
            idx = 0
        if idx < 0:
            idx = 0
        hass.services.call(
            "media_player",
            "play_media",
            {
                "entity_id": player,
                "media_content_id": radios[idx].get(CONF_NETRADIO_RADIO_URL),
                "media_content_type": MIME_TYPE,
            },
            False,
        )

    def prev_radio(service):
        """Switch radio to previous player entity."""
        player = service.data.get(ATTR_PLAYER_ENTITY)
        radios = config[DOMAIN][CONF_NETRADIO_RADIOS]
        url: string = hass.states.get(player).attributes.get(ATTR_MEDIA_CONTENT_ID)
        idx: int = 0
        for i in radios:
            if i.get("url") == url:
                idx = radios.index(i)
        idx = idx - 1
        if idx >= len(radios):
            idx = 0
        if idx < 0:
            idx = 0
        hass.services.call(
            "media_player",
            "play_media",
            {
                "entity_id": player,
                "media_content_id": radios[idx].get(CONF_NETRADIO_RADIO_URL),
                "media_content_type": MIME_TYPE,
            },
            False,
        )

    hass.data[DOMAIN] = {}

    # Create the NetRadio Source
    _LOGGER.info("NetRadio setting up")
    radios = config[DOMAIN][CONF_NETRADIO_RADIOS]
    source = NetRadioSource(hass, radios)
    hass.data[DOMAIN][DOMAIN] = source
    hass.states.async_set("netradio.netradio", "Initialized", {"radios": radios})

    # Register the services
    hass.services.async_register(
        DOMAIN,
        SERVICE_START_RADIO,
        start_radio,
        schema=SERVICE_START_RADIO_SCHEMA,
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_NEXT_RADIO,
        next_radio,
        schema=SERVICE_NEXT_RADIO_SCHEMA,
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_PREV_RADIO,
        prev_radio,
        schema=SERVICE_NEXT_RADIO_SCHEMA,
    )

    return True
