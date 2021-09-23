from .abc import Provider


class MapProvider(Provider):
    # pylint: disable=arguments-renamed
    async def fetch(self, latlon: str) -> dict:
        url = (
            "https://tux-maps-prod.gnous.eu/v1/staticmap"
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

        return {"bytes": None, "url": output}
