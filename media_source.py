"""NetRadio Media Source Implementation."""

from homeassistant.components.climate.const import ATTR_HVAC_MODE
import logging

from homeassistant.components.media_player.const import (
    MEDIA_CLASS_DIRECTORY,
    MEDIA_CLASS_MUSIC,
    MEDIA_TYPE_MUSIC,
)

from homeassistant.core import HomeAssistant
from homeassistant.components.media_player.errors import BrowseError
from homeassistant.components.media_source.const import MEDIA_MIME_TYPES
from homeassistant.components.media_source.error import MediaSourceError, Unresolvable
from homeassistant.components.media_source.models import (
    BrowseMediaSource,
    MediaSource,
    MediaSourceItem,
    PlayMedia,
)


from .const import MIME_TYPE, DOMAIN, ENTITY_ID


_LOGGER = logging.getLogger(__name__)


async def async_get_media_source(hass: HomeAssistant):
    """Set up NetRadio media source."""
    #    _LOGGER.info("NetRadio setting up:" + DOMAIN)
    source = hass.data[DOMAIN][DOMAIN]
    return source


class NetRadioSource(MediaSource):
    """Provide NetRadio URLs as media sources."""

    entity_id = ENTITY_ID

    _radios: list

    @property
    def radios(self):
        """Return the list of configured net radios URLs."""
        return self._radios

    def __init__(self, hass: HomeAssistant, radios: list):
        """Initialize NetRadio source."""
        super().__init__(DOMAIN)
        self.hass = hass
        self._radios = radios
        self._state = "Starting"

    async def async_resolve_media(self, item: MediaSourceItem) -> PlayMedia:
        """Resolve media to a url."""
        url = item.identifier
        _LOGGER.info("NetRadio resolve media: " + url)
        return PlayMedia(url, MIME_TYPE)

    async def async_browse_media(self, item: MediaSourceItem) -> BrowseMediaSource:
        """Return media."""
        return self._browse_media(item.identifier)

    def _browse_media(self, source: str) -> BrowseMediaSource:
        """Browse media."""
        # If only one media dir is configured, use that as the local media root
        if source == "" or source is None:
            source = "Netradio"

        media = BrowseMediaSource(
            domain=DOMAIN,
            identifier=source,
            media_class=MEDIA_CLASS_DIRECTORY,
            media_content_type="",
            title="Netradio",
            can_play=False,
            can_expand=True,
            thumbnail=None,
        )

        # Append first level children
        media.children = []
        for child_name in self._radios:
            child = BrowseMediaSource(
                domain=DOMAIN,
                identifier=child_name.get("url"),
                media_class=MEDIA_CLASS_MUSIC,
                media_content_type=MEDIA_TYPE_MUSIC,
                title=child_name.get("name") + " URL: " + child_name.get("url"),
                can_play=True,
                can_expand=False,
            )
            media.children.append(child)

        _LOGGER.info("Browse media completed")
        return media

    @property
    def name(self):
        """Return the name."""
        return "NetRadio"
