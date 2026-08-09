import asyncio
import json
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime, timezone

from settings import *


class LeaderboardManager:

    def __init__(self):

        self.url = (
            SUPABASE_URL
            + "/rest/v1/leaderboard"
        )

        self.headers = {
            "apikey": SUPABASE_KEY,

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

        print("========================================")
        print("LEADERBOARD MANAGER INITIALIZED")
        print("Supabase URL:", SUPABASE_URL)
        print("Leaderboard URL:", self.url)
        print("========================================")


    # ============================================================
    # GENERIC ASYNC REQUEST
    # ============================================================

    async def request(
        self,
        method,
        data=None,
        params=""
    ):

        full_url = self.url + params

        print("")
        print("========================================")
        print("SUPABASE REQUEST")
        print("Method:", method)
        print("URL:", full_url)

        if data is not None:
            print("Data:", json.dumps(data, indent=4))

        print("========================================")

        return await asyncio.to_thread(
            self._request_urllib,
            full_url,
            method,
            data
        )


    # ============================================================
    # SYNCHRONOUS HTTP REQUEST
    # Runs inside asyncio.to_thread()
    # ============================================================

    def _request_urllib(
        self,
        full_url,
        method,
        data=None
    ):

        try:

            headers = dict(self.headers)

            # Supabase should return the created/updated row.
            if method in ("POST", "PATCH"):
                headers["Prefer"] = "return=representation"

            body = None

            if data is not None:

                body = json.dumps(
                    data
                ).encode("utf-8")

            request = urllib.request.Request(
                full_url,
                data=body,
                method=method,
                headers=headers
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
            print("Status:", status)
            print("Raw response:", raw)
            print("========================================")

            if not raw:

                self.last_response = []

                return []

            try:

                parsed = json.loads(raw)

            except json.JSONDecodeError:

                parsed = raw

            self.last_response = parsed

            return parsed


        except urllib.error.HTTPError as error:

            try:
                body = error.read().decode(
                    "utf-8"
                )
            except Exception:
                body = ""

            error_text = (
                f"HTTP {error.code}: {body}"
            )

            print("")
            print("========================================")
            print("SUPABASE HTTP ERROR")
            print(error_text)
            print("========================================")

            self.last_status = error.code
            self.last_response = body
            self.last_error = error_text

            return []


        except urllib.error.URLError as error:

            error_text = (
                f"URL ERROR: {error}"
            )

            print("")
            print("========================================")
            print("SUPABASE URL ERROR")
            print(error_text)
            print("========================================")

            self.last_status = None
            self.last_response = None
            self.last_error = error_text

            return []


        except Exception as error:

            error_text = (
                f"{type(error).__name__}: {error}"
            )

            print("")
            print("========================================")
            print("SUPABASE REQUEST ERROR")
            print(error_text)
            print("========================================")

            self.last_status = None
            self.last_response = None
            self.last_error = error_text

            return []


    # ============================================================
    # GET EXISTING PLAYER SCORE
    # ============================================================

    async def get_player_score(
        self,
        name
    ):

        print("")
        print("========================================")
        print("CHECKING EXISTING PLAYER SCORE")
        print("Player:", name)
        print("========================================")

        safe_name = urllib.parse.quote(
            str(name),
            safe=""
        )

        params = (
            f"?name=eq.{safe_name}"
            "&select=id,name,score,level,time"
        )

        result = await self.request(
            "GET",
            params=params
        )

        # Supabase SELECT should return a list.
        if not isinstance(result, list):

            print(
                "Unexpected Supabase response type:",
                type(result)
            )

            return None

        if len(result) == 0:

            print(
                "No existing score found for:",
                name
            )

            return None

        # Find the best existing entry.
        valid_rows = []

        for row in result:

            if not isinstance(row, dict):
                continue

            valid_rows.append(row)

        if not valid_rows:

            print(
                "Supabase returned rows, but none "
                "were dictionaries."
            )

            return None

        best = max(
            valid_rows,
            key=lambda row: (
                int(row.get("level", 0) or 0),
                int(row.get("score", 0) or 0)
            )
        )

        print("Existing best score:")
        print(best)

        return best


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
        print("########################################")
        print("SUBMIT SCORE")
        print("Name:", name)
        print("Score:", score)
        print("Level:", level)
        print("########################################")

        # --------------------------------------------------------
        # Validate values
        # --------------------------------------------------------

        try:

            name = str(name).strip()
            score = int(score)
            level = int(level)

        except Exception as error:

            print(
                "Invalid score data:",
                error
            )

            return False

        if not name:

            print(
                "ERROR: Player name is empty."
            )

            return False

        if score < 0:

            print(
                "ERROR: Score cannot be negative."
            )

            return False

        if level < 1:

            print(
                "ERROR: Level must be at least 1."
            )

            return False

        # --------------------------------------------------------
        # Check existing score
        # --------------------------------------------------------

        existing = await self.get_player_score(
            name
        )

        # --------------------------------------------------------
        # Generate timestamp
        # --------------------------------------------------------

        current_time = datetime.now(
            timezone.utc
        ).isoformat()

        print(
            "Timestamp:",
            current_time
        )

        # ========================================================
        # NO EXISTING SCORE
        # ========================================================

        if existing is None:

            print("")
            print("NO EXISTING SCORE.")
            print("INSERTING NEW SCORE...")

            payload = {
                "name": name,
                "score": score,
                "level": level,
                "time": current_time
            }

            result = await self.request(
                "POST",
                data=payload
            )

            if (
                self.last_status is not None
                and
                200 <= int(self.last_status) < 300
            ):

                print("")
                print("########################################")
                print("SUCCESS!")
                print("NEW SCORE INSERTED INTO SUPABASE")
                print("########################################")

                return True

            print("")
            print("########################################")
            print("INSERT FAILED")
            print("Error:", self.last_error)
            print("########################################")

            return False

        # ========================================================
        # EXISTING SCORE
        # ========================================================

        try:

            old_level = int(
                existing.get("level", 0) or 0
            )

            old_score = int(
                existing.get("score", 0) or 0
            )

        except Exception as error:

            print(
                "ERROR READING EXISTING SCORE:",
                error
            )

            return False

        print("")
        print("EXISTING SCORE FOUND")
        print("Old level:", old_level)
        print("Old score:", old_score)
        print("New level:", level)
        print("New score:", score)

        # --------------------------------------------------------
        # Determine whether new score is better
        # --------------------------------------------------------

        better_level = (
            level > old_level
        )

        same_level_better_score = (
            level == old_level
            and
            score > old_score
        )

        if not (
            better_level
            or
            same_level_better_score
        ):

            print("")
            print(
                "NEW SCORE IS NOT BETTER."
            )

            print(
                "Keeping existing leaderboard entry."
            )

            return False

        # ========================================================
        # UPDATE EXISTING SCORE
        # ========================================================

        row_id = existing.get("id")

        if row_id is None:

            print(
                "ERROR: Existing score has no ID."
            )

            return False

        payload = {
            "name": name,
            "score": score,
            "level": level,
            "time": current_time
        }

        print("")
        print("NEW SCORE IS BETTER!")
        print("UPDATING SUPABASE ROW...")
        print("Row ID:", row_id)

        params = (
            f"?id=eq.{urllib.parse.quote(str(row_id))}"
        )

        result = await self.request(
            "PATCH",
            data=payload,
            params=params
        )

        if (
            self.last_status is not None
            and
            200 <= int(self.last_status) < 300
        ):

            print("")
            print("########################################")
            print("SUCCESS!")
            print("SCORE UPDATED IN SUPABASE")
            print("########################################")

            return True

        print("")
        print("########################################")
        print("UPDATE FAILED")
        print("Error:", self.last_error)
        print("########################################")

        return False


    # ============================================================
    # GET TOP 10 SCORES
    # ============================================================

    async def get_top_scores(self):

        print("")
        print("========================================")
        print("GET TOP 10 SCORES")
        print("========================================")

        params = (
            "?select=id,name,score,level,time"
            "&order=level.desc,score.desc"
            "&limit=10"
        )

        scores = await self.request(
            "GET",
            params=params
        )

        if not isinstance(scores, list):

            print(
                "ERROR: Expected leaderboard list."
            )

            return []

        print(
            "Leaderboard entries:",
            len(scores)
        )

        return scores


    # ============================================================
    # GET PLAYER RANK
    # ============================================================

    async def get_player_rank(
        self,
        name
    ):

        print("")
        print("========================================")
        print("GET PLAYER RANK")
        print("Player:", name)
        print("========================================")

        params = (
            "?select=id,name,score,level,time"
            "&order=level.desc,score.desc"
        )

        players = await self.request(
            "GET",
            params=params
        )

        if not isinstance(players, list):

            print(
                "ERROR: Expected player list."
            )

            return None, None

        for index, player in enumerate(
            players,
            start=1
        ):

            if not isinstance(player, dict):
                continue

            if player.get("name") == name:

                print(
                    "Player rank:",
                    index
                )

                return index, player

        print(
            "Player not found on leaderboard."
        )

        return None, None