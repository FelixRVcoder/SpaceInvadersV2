import asyncio
import json
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime

from settings import *


class LeaderboardManager:

    def __init__(self):

        self.url = (
            SUPABASE_URL
            + "/rest/v1/leaderboard"
        )

        self.headers = {

            "apikey":
            SUPABASE_KEY,

            "Authorization":
            "Bearer " + SUPABASE_KEY,

            "Content-Type":
            "application/json",

            "Accept":
            "application/json"
        }

        # Diagnostic information
        self.last_status = None
        self.last_response = None
        self.last_error = None


    async def request(
        self,
        method,
        data=None,
        params=""
    ):

        # Reset diagnostic information for EVERY request.
        self.last_status = None
        self.last_response = None
        self.last_error = None

        # Pygbag/browser builds can strip custom headers.
        # Putting the API key in the URL makes the request
        # work reliably in the browser version too.

        separator = "&" if "?" in params else "?"

        full_url = (
            self.url
            + params
            + separator
            + urllib.parse.urlencode(
                {
                    "apikey": SUPABASE_KEY
                }
            )
        )

        print(
            "SUPABASE REQUEST:",
            method,
            full_url
        )

        return await asyncio.to_thread(
            self._request_urllib,
            full_url,
            method,
            data
        )


    def _request_urllib(
        self,
        full_url,
        method,
        data=None
    ):

        try:

            headers = dict(self.headers)

            if data is not None:

                headers["Prefer"] = (
                    "return=representation"
                )

            req = urllib.request.Request(
                full_url,
                method=method,
                headers=headers
            )

            if data is not None:

                req.data = json.dumps(
                    data
                ).encode(
                    "utf-8"
                )

                print(
                    "SUPABASE DATA:",
                    data
                )

            with urllib.request.urlopen(
                req,
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

                print(
                    "SUPABASE RESPONSE:",
                    raw
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

                body = he.read().decode(
                    "utf-8"
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

        print()
        print(
            "================================"
        )
        print(
            "        SUBMITTING SCORE"
        )
        print(
            "================================"
        )

        print(
            "NAME:",
            name
        )

        print(
            "SCORE:",
            score
        )

        print(
            "LEVEL:",
            level
        )


        # Your Supabase column is currently:
        #
        # timestamp
        #
        # This is PostgreSQL timestamp WITHOUT timezone.
        #
        # Example:
        # 2026-08-09 17:25:43

        current_time = (
            datetime.now()
            .strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )

        print(
            "TIME:",
            current_time
        )


        # Safely encode the player's name
        # for the PostgREST filter.

        safe_name = urllib.parse.quote(
            name,
            safe=""
        )


        print()
        print(
            "CHECKING FOR EXISTING PLAYER..."
        )


        existing = await self.request(

            "GET",

            params=(
                "?name=eq."
                + safe_name
            )

        )


        print(
            "EXISTING RESULT:",
            existing
        )

        print(
            "EXISTING TYPE:",
            type(existing)
        )


        # ==================================================
        # NO EXISTING PLAYER
        # ==================================================

        if not existing:

            print()
            print(
                "NO EXISTING PLAYER FOUND."
            )

            print(
                "SENDING POST..."
            )


            result = await self.request(

                "POST",

                {
                    "name":
                    name,

                    "score":
                    score,

                    "level":
                    level,

                    "time":
                    current_time
                }

            )


            print()
            print(
                "POST RESULT:",
                result
            )

            print(
                "POST STATUS:",
                self.last_status
            )

            print(
                "POST ERROR:",
                self.last_error
            )


        # ==================================================
        # EXISTING PLAYER
        # ==================================================

        else:

            # Make sure we actually received
            # a list containing dictionaries.

            if not isinstance(
                existing,
                list
            ):

                print(
                    "ERROR: Supabase returned "
                    "unexpected data."
                )

                print(
                    "DATA:",
                    existing
                )

                return False


            if not isinstance(
                existing[0],
                dict
            ):

                print(
                    "ERROR: Player data is "
                    "not a dictionary."
                )

                print(
                    "DATA:",
                    existing[0]
                )

                return False


            old = existing[0]


            old_score = old.get(
                "score",
                0
            )

            old_level = old.get(
                "level",
                0
            )


            print()
            print(
                "EXISTING PLAYER FOUND"
            )

            print(
                "OLD SCORE:",
                old_score
            )

            print(
                "OLD LEVEL:",
                old_level
            )


            better_score = (
                score > old_score
            )

            better_level = (
                level > old_level
            )


            print(
                "BETTER SCORE:",
                better_score
            )

            print(
                "BETTER LEVEL:",
                better_level
            )


            # ==================================================
            # NEW SCORE IS BETTER
            # ==================================================

            if (
                better_score
                or
                better_level
            ):

                print()
                print(
                    "NEW RECORD!"
                )

                print(
                    "SENDING PATCH..."
                )


                result = await self.request(

                    "PATCH",

                    {
                        "score":
                        score,

                        "level":
                        level,

                        "time":
                        current_time
                    },

                    params=(
                        "?name=eq."
                        + safe_name
                    )

                )


                print()
                print(
                    "PATCH RESULT:",
                    result
                )

                print(
                    "PATCH STATUS:",
                    self.last_status
                )

                print(
                    "PATCH ERROR:",
                    self.last_error
                )


            # ==================================================
            # NEW SCORE IS NOT BETTER
            # ==================================================

            else:

                print()
                print(
                    "SCORE NOT BETTER THAN "
                    "EXISTING RECORD."
                )

                print(
                    "NO PATCH NEEDED."
                )


        print()
        print(
            "================================"
        )

        print(
            "        SUBMIT COMPLETE"
        )

        print(
            "================================"
        )

        print()


        # Only report success if the actual
        # POST/PATCH request succeeded.

        if (
            self.last_status is not None
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


        # This happens when no POST/PATCH
        # was necessary.

        return False


    async def get_top_scores(
        self
    ):

        print(
            "GET TOP SCORES"
        )


        scores = await self.request(

            "GET",

            params=(
                "?order="
                "level.desc,"
                "score.desc"
                "&limit=10"
            )

        )


        print(
            "TOP SCORES RESULT:",
            scores
        )


        # Never allow a string/error response
        # to reach LeaderboardScreen.

        if not isinstance(
            scores,
            list
        ):

            print(
                "TOP SCORES ERROR:"
                " unexpected response."
            )

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
                "?order="
                "level.desc,"
                "score.desc"
            )

        )


        if not isinstance(
            players,
            list
        ):

            print(
                "PLAYER RANK ERROR:"
                " unexpected response."
            )

            return None, None


        for index, player in enumerate(
            players,
            start=1
        ):

            if not isinstance(
                player,
                dict
            ):

                continue


            if player.get(
                "name"
            ) == name:

                return index, player


        return None, None