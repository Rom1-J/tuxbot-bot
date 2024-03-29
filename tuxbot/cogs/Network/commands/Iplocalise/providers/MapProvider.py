import typing

from .abc import Provider


class MapProvider(Provider):
    # pylint: disable=arguments-renamed
    async def fetch(self, latlon: str) -> tuple[str, dict[str, typing.Any]]:
        url = (
            "https://maps.geoapify.com/v1/staticmap"
            "?style=osm-carto"
            "&width=333"
            "&height=250"
            "&center=lonlat:{lonlat}"
            "&zoom=10"
            "&marker=lonlat:{lonlat};color:%23ff0000;size:small"
            "&apiKey={apikey}"
        )

        lonlat = ",".join(latlon.split(",")[::-1])

        output = url.format(lonlat=lonlat, apikey=self.apikey)

        return "map", {"bytes": None, "url": output}
