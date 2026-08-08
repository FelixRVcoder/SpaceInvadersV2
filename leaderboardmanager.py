import asyncio
import json
import sys
import urllib.parse

from settings import *


class LeaderboardManager:

    def __init__(self):

        self.url = (
            SUPABASE_URL
            +
            "/rest/v1/leaderboard"
        )

        self.headers = {

            "apikey":
            SUPABASE_KEY,

            "Authorization":
            "Bearer " + SUPABASE_KEY,

            "Content-Type":
            "application/json; charset=utf-8",

            "Accept":
            "application/json"

        }

        self.last_status = None

        self.last_response = None

        self.last_error = None

        self.is_web = (
            sys.platform == "emscripten"
        )

    async def request(
        self,
        method,
        data=None,
        params=""
    ):

        full_url = self.url + params

        print(
            "SUPABASE REQUEST:",
            method,
            full_url
        )

        if self.is_web:

            return await self._request_web(
                full_url,
                method,
                data
            )

        return await asyncio.to_thread(
            self._request_desktop,
            full_url,
            method,
            data
        )

    async def _request_web(
        self,
        full_url,
        method,
        data=None
    ):

        try:

            import platform

            await asyncio.sleep(0)

            # ---------------------------------
            # GET
            # ---------------------------------

            if method == "GET":

                result = await platform.jsiter(

                    platform.window.Fetch.GET(
                        full_url
                    )

                )

            # ---------------------------------
            # POST
            # ---------------------------------

            elif method == "POST":

                payload = json.dumps(
                    data
                    if data is not None
                    else {}
                )

                result = await platform.jsiter(

                    platform.window.Fetch.POST(
                        full_url,
                        payload
                    )

                )

            # ---------------------------------
            # PATCH
            # ---------------------------------

            else:

                # The pygbag Fetch helper exposes
                # GET and POST directly. For PATCH,
                # use the browser's native fetch API.

                options = {

                    "method":
                    method,

                    "headers":
                    self.headers,

                    "body":
                    json.dumps(data)
                    if data is not None
                    else None

                }

                result = await platform.jsiter(

                    platform.window.fetch(
                        full_url,
                        options
                    )

                )

                try:

                    result = await platform.jsiter(
                        result.text()
                    )

                except Exception:

                    pass

            self.last_error = None

            self.last_response = result

            self.last_status = 200

            print(
                "SUPABASE RESPONSE:",
                result
            )

            if isinstance(
                result,
                str
            ):

                try:

                    return json.loads(
                        result
                    )

                except Exception:

                    return result

            return result

        except Exception as e:

            error_text = str(e)

            print(
                "SUPABASE WEB ERROR:",
                error_text
            )

            self.last_status = None

            self.last_response = None

            self.last_error = error_text

            return []

    def _request_desktop(
        self,
        full_url,
        method,
        data=None
    ):

        import urllib.request
        import urllib.error

        try:

            headers = dict(
                self.headers
            )

            if data is not None:

                headers["Prefer"] = (
                    "return=representation"
                )

            request = urllib.request.Request(

                full_url,

                method=method,

                headers=headers

            )

            if data is not None:

                request.data = json.dumps(
                    data
                ).encode(
                    "utf-8"
                )

            with urllib.request.urlopen(
                request,
                timeout=10
            ) as response:

                status = response.getcode()

                self.last_status = status

                self.last_error = None

                raw = response.read().decode(
                    "utf-8"
                )

                print(
                    "SUPABASE STATUS:",
                    status
                )

                if raw:

                    try:

                        parsed = json.loads(
                            raw
                        )

                    except Exception:

                        parsed = raw

                    self.last_response = parsed

                    return parsed

                self.last_response = None

                return []

        except urllib.error.HTTPError as he:

            try:

                body = (
                    he.read()
                    .decode(
                        "utf-8"
                    )
                )

            except Exception:

                body = None

            error_text = (
                f"HTTP {he.code}: {body}"
            )

            print(
                "SUPABASE HTTP ERROR:",
                error_text
            )

            self.last_status = he.code

            self.last_response = body

            self.last_error = error_text

            return []

        except Exception as e:

            error_text = str(e)

            print(
                "SUPABASE ERROR:",
                error_text
            )

            self.last_status = None

            self.last_response = None

            self.last_error = error_text

            return []

    async def submit_score(
        self,
        name,
        score,
        level
    ):

        print(
            "SUBMIT SCORE:",
            name,
            score,
            level
        )

        safe_name = urllib.parse.quote(
            name,
            safe=""
        )

        existing = await self.request(

            "GET",

            params=(
                f"?name=eq.{safe_name}"
            )

        )

        if existing:

            old = existing[0]

            better_score = (

                score > old.get(
                    "score",
                    0
                )

            )

            better_level = (

                level > old.get(
                    "level",
                    0
                )

            )

            if better_score or better_level:

                await self.request(

                    "PATCH",

                    {

                        "score":
                        score,

                        "level":
                        level

                    },

                    f"?name=eq.{safe_name}"

                )

        else:

            await self.request(

                "POST",

                {

                    "name":
                    name,

                    "score":
                    score,

                    "level":
                    level

                }

            )

        print(
            "SUBMIT COMPLETE"
        )

        if (
            self.last_status
            and
            200 <= int(
                self.last_status
            ) < 300
        ):

            return True

        if self.last_error is not None:

            print(
                "SUBMIT FAILED:",
                self.last_error
            )

            return False

        return True

    async def get_top_scores(
        self
    ):

        print(
            "GET TOP SCORES"
        )

        scores = await self.request(

            "GET",

            params=(
                "?order=level.desc,"
                "score.desc&limit=10"
            )

        )

        if not scores:

            return []

        return scores

    async def get_player_rank(
        self,
        name
    ):

        print(
            "GET PLAYER RANK"
        )

        players = await self.request(

            "GET",

            params=(
                "?order=level.desc,"
                "score.desc"
            )

        )

        if not players:

            return None, None

        for index, player in enumerate(

            players,

            start=1

        ):

            if player.get(
                "name"
            ) == name:

                return index, player

        return None, None