import asyncio
import json
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime

from settings import *


class LeaderboardManager:

    def __init__(self):

        self.base_url = (
            SUPABASE_URL.rstrip("/")
            + "/rest/v1/leaderboard"
        )

        self.last_status = None
        self.last_response = None
        self.last_error = None

        print("")
        print("========================================")
        print("LEADERBOARD MANAGER")
        print("========================================")
        print("Supabase URL:", SUPABASE_URL)
        print("Table URL:", self.base_url)
        print("========================================")


    # ============================================================
    # ASYNC REQUEST
    # ============================================================

    async def request(
        self,
        method,
        data=None,
        params=""
    ):

        return await asyncio.to_thread(
            self._request,
            method,
            data,
            params
        )


    # ============================================================
    # ACTUAL HTTP REQUEST
    # ============================================================

    def _request(
        self,
        method,
        data=None,
        params=""
    ):

        try:

            # ----------------------------------------------------
            # IMPORTANT:
            #
            # Put the API key in the URL because previous
            # successful Pygbag requests showed that this works.
            # ----------------------------------------------------

            separator = "&" if "?" in params else "?"

            url = (
                self.base_url
                + params
                + separator
                + "apikey="
                + urllib.parse.quote(
                    SUPABASE_KEY,
                    safe=""
                )
            )

            print("")
            print("========================================")
            print("SUPABASE REQUEST")
            print("METHOD:", method)
            print("URL:", url)

            if data is not None:

                print(
                    "DATA:",
                    json.dumps(
                        data,
                        indent=4
                    )
                )

            print("========================================")

            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }

            # ----------------------------------------------------
            # Authorization
            #
            # Keep it as Bearer as well. The URL apikey is the
            # important part for our Pygbag test.
            # ----------------------------------------------------

            headers["Authorization"] = (
                "Bearer " + SUPABASE_KEY
            )

            body = None

            if data is not None:

                body = json.dumps(
                    data
                ).encode("utf-8")

            request = urllib.request.Request(
                url,
                data=body,
                headers=headers,
                method=method
            )

            with urllib.request.urlopen(
                request,
                timeout=10
            ) as response:

                status = response.getcode()

                raw = response.read().decode(
                    "utf-8"
                )

            self.last_status = status
            self.last_error = None

            print("")
            print("========================================")
            print("SUPABASE RESPONSE")
            print("STATUS:", status)
            print("BODY:", raw)
            print("========================================")

            if not raw:

                self.last_response = []

                return []

            try:

                result = json.loads(raw)

            except json.JSONDecodeError:

                result = raw

            self.last_response = result

            return result


        except urllib.error.HTTPError as error:

            try:

                body = error.read().decode(
                    "utf-8"
                )

            except Exception:

                body = ""

            self.last_status = error.code
            self.last_response = body

            self.last_error = (
                f"HTTP {error.code}: {body}"
            )

            print("")
            print("========================================")
            print("SUPABASE HTTP ERROR")
            print("STATUS:", error.code)
            print("BODY:", body)
            print("========================================")

            return []


        except Exception as error:

            self.last_status = None
            self.last_response = None

            self.last_error = (
                f"{type(error).__name__}: {error}"
            )

            print("")
            print("========================================")
            print("SUPABASE CONNECTION ERROR")
            print(self.last_error)
            print("========================================")

            return []


    # ============================================================
    # SUBMIT SCORE
    # ============================================================

    async def submit_score(
        self,
        name,
        score,
        level
    ):

        print("")
        print("")
        print("########################################")
        print("STARTING SCORE SUBMISSION")
        print("########################################")
        print("NAME:", name)
        print("SCORE:", score)
        print("LEVEL:", level)

        # --------------------------------------------------------
        # Clean values
        # --------------------------------------------------------

        name = str(name).strip()
        score = int(score)
        level = int(level)

        if not name:

            print("ERROR: Empty player name.")
            return False

        # --------------------------------------------------------
        # STEP 1: Check whether player already exists
        # --------------------------------------------------------

        safe_name = urllib.parse.quote(
            name,
            safe=""
        )

        existing = await self.request(
            "GET",
            params=(
                "?name=eq."
                + safe_name
                + "&select=id,name,score,level,time"
            )
        )

        print("")
        print("EXISTING PLAYER RESULT:")
        print(existing)

        # ========================================================
        # PLAYER DOES NOT EXIST
        # ========================================================

        if isinstance(existing, list) and len(existing) == 0:

            print("")
            print("PLAYER DOES NOT EXIST.")
            print("ATTEMPTING POST...")

            # Your current column is `timestamp` without timezone,
            # so send a plain PostgreSQL-compatible timestamp.
            current_time = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            payload = {
                "name": name,
                "score": score,
                "level": level,
                "time": current_time
            }

            result = await self.request(
                "POST",
                data=payload,
                params=""
            )

            print("")
            print("POST RESULT:")
            print(result)

            if (
                self.last_status is not None
                and
                200 <= self.last_status < 300
            ):

                print("")
                print("########################################")
                print("POST SUCCESS")
                print("SCORE WAS INSERTED")
                print("########################################")

                return True

            print("")
            print("########################################")
            print("POST FAILED")
            print("########################################")
            print("STATUS:", self.last_status)
            print("ERROR:", self.last_error)

            return False

        # ========================================================
        # EXISTING PLAYER
        # ========================================================

        if not isinstance(existing, list):

            print(
                "ERROR: Unexpected GET response."
            )

            return False

        if len(existing) == 0:

            print(
                "ERROR: Could not determine player state."
            )

            return False

        old = existing[0]

        old_score = int(
            old.get("score", 0)
        )

        old_level = int(
            old.get("level", 0)
        )

        print("")
        print("PLAYER ALREADY EXISTS")
        print("OLD SCORE:", old_score)
        print("OLD LEVEL:", old_level)

        # --------------------------------------------------------
        # Determine whether new score is better
        # --------------------------------------------------------

        better = False

        if level > old_level:

            better = True

        elif (
            level == old_level
            and score > old_score
        ):

            better = True

        if not better:

            print("")
            print("NEW SCORE IS NOT BETTER.")
            print("NOTHING WILL BE UPDATED.")

            return False

        # --------------------------------------------------------
        # UPDATE
        # --------------------------------------------------------

        row_id = old.get("id")

        if row_id is None:

            print(
                "ERROR: Existing row has no ID."
            )

            return False

        current_time = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        payload = {
            "name": name,
            "score": score,
            "level": level,
            "time": current_time
        }

        print("")
        print("NEW SCORE IS BETTER.")
        print("ATTEMPTING PATCH...")
        print("ROW ID:", row_id)

        result = await self.request(
            "PATCH",
            data=payload,
            params=(
                "?id=eq."
                + urllib.parse.quote(
                    str(row_id),
                    safe=""
                )
            )
        )

        print("")
        print("PATCH RESULT:")
        print(result)

        if (
            self.last_status is not None
            and
            200 <= self.last_status < 300
        ):

            print("")
            print("########################################")
            print("PATCH SUCCESS")
            print("SCORE WAS UPDATED")
            print("########################################")

            return True

        print("")
        print("########################################")
        print("PATCH FAILED")
        print("########################################")
        print("STATUS:", self.last_status)
        print("ERROR:", self.last_error)

        return False


    # ============================================================
    # TOP 10
    # ============================================================

    async def get_top_scores(self):

        print("")
        print("========================================")
        print("GETTING TOP SCORES")
        print("========================================")

        result = await self.request(
            "GET",
            params=(
                "?select=id,name,score,level,time"
                "&order=level.desc,score.desc"
                "&limit=10"
            )
        )

        if not isinstance(result, list):

            print(
                "ERROR: Leaderboard response is not a list."
            )

            return []

        print(
            "TOP SCORES RECEIVED:",
            len(result)
        )

        return result


    # ============================================================
    # PLAYER RANK
    # ============================================================

    async def get_player_rank(
        self,
        name
    ):

        print("")
        print("========================================")
        print("GETTING PLAYER RANK")
        print("PLAYER:", name)
        print("========================================")

        result = await self.request(
            "GET",
            params=(
                "?select=id,name,score,level,time"
                "&order=level.desc,score.desc"
            )
        )

        if not isinstance(result, list):

            print(
                "ERROR: Rank response is not a list."
            )

            return None, None

        for index, player in enumerate(
            result,
            start=1
        ):

            if (
                isinstance(player, dict)
                and
                player.get("name") == name
            ):

                print(
                    "PLAYER RANK:",
                    index
                )

                return index, player

        print(
            "PLAYER NOT FOUND IN LEADERBOARD"
        )

        return None, None