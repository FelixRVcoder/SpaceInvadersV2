import json
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime, timezone


class LeaderboardManager:
    # ============================================================
    # SUPABASE CONFIGURATION
    # ============================================================

    SUPABASE_URL = "https://bzrqnprelyfkxusehxcv.supabase.co"

    # IMPORTANT:
    # Put your Supabase PUBLISHABLE key here.
    #
    # Use the same sb_publishable_... key that you were previously
    # using successfully in your browser GET request.
    SUPABASE_KEY = "YOUR_SUPABASE_PUBLISHABLE_KEY"

    TABLE_NAME = "leaderboard"

    # ============================================================
    # INITIALIZATION
    # ============================================================

    def __init__(self):
        self.base_url = (
            f"{self.SUPABASE_URL}/rest/v1/{self.TABLE_NAME}"
        )

        print("========================================")
        print("LEADERBOARD MANAGER INITIALIZED")
        print("Supabase URL:", self.SUPABASE_URL)
        print("Table:", self.TABLE_NAME)
        print("========================================")

    # ============================================================
    # HEADERS
    # ============================================================

    def _headers(self, include_content_type=False):
        headers = {
            "apikey": self.SUPABASE_KEY,
            "Authorization": f"Bearer {self.SUPABASE_KEY}",
            "Accept": "application/json",
        }

        if include_content_type:
            headers["Content-Type"] = "application/json"
            headers["Prefer"] = "return=representation"

        return headers

    # ============================================================
    # GET LEADERBOARD
    # ============================================================

    def get_leaderboard(self):
        """
        Gets all leaderboard entries from Supabase.

        Sorting:
        1. Highest level first
        2. Highest score first
        """

        try:
            print("========================================")
            print("GETTING LEADERBOARD FROM SUPABASE...")
            print("URL:", self.base_url)
            print("========================================")

            params = urllib.parse.urlencode({
                "select": "id,name,score,level,time",
                "order": "level.desc,score.desc"
            })

            url = f"{self.base_url}?{params}"

            request = urllib.request.Request(
                url,
                headers=self._headers(),
                method="GET"
            )

            with urllib.request.urlopen(request, timeout=10) as response:
                status = response.status
                raw_data = response.read().decode("utf-8")

            print("Supabase GET status:", status)
            print("Supabase GET response:", raw_data)

            if not raw_data:
                print("Supabase returned an empty response.")
                return []

            try:
                data = json.loads(raw_data)
            except json.JSONDecodeError:
                print("ERROR: Supabase returned invalid JSON.")
                print("Raw response:", raw_data)
                return []

            # Supabase normally returns a LIST for SELECT.
            if not isinstance(data, list):
                print("ERROR: Expected a list from Supabase.")
                print("Received:", type(data))
                print("Data:", data)
                return []

            print("Leaderboard entries received:", len(data))

            return data

        except urllib.error.HTTPError as e:
            print("========================================")
            print("SUPABASE GET HTTP ERROR")
            print("Status:", e.code)

            try:
                error_body = e.read().decode("utf-8")
                print("Response:", error_body)
            except Exception:
                pass

            print("========================================")

            return []

        except urllib.error.URLError as e:
            print("========================================")
            print("SUPABASE GET URL ERROR")
            print(e)
            print("========================================")

            return []

        except Exception as e:
            print("========================================")
            print("SUPABASE GET ERROR")
            print(type(e).__name__, ":", e)
            print("========================================")

            return []

    # ============================================================
    # GET SCORE FOR A SPECIFIC PLAYER
    # ============================================================

    def get_player_score(self, name):
        """
        Gets the existing leaderboard entry for a player.
        """

        try:
            encoded_name = urllib.parse.quote(str(name), safe="")

            url = (
                f"{self.base_url}"
                f"?name=eq.{encoded_name}"
                f"&select=id,name,score,level,time"
            )

            print("Checking existing score for:", name)
            print("URL:", url)

            request = urllib.request.Request(
                url,
                headers=self._headers(),
                method="GET"
            )

            with urllib.request.urlopen(request, timeout=10) as response:
                raw_data = response.read().decode("utf-8")

            print("Existing-score response:", raw_data)

            data = json.loads(raw_data)

            if not isinstance(data, list):
                print("Unexpected existing-score response.")
                return None

            if len(data) == 0:
                print("No existing score found for:", name)
                return None

            # If somehow there are multiple rows with the same name,
            # choose the best one.
            best = max(
                data,
                key=lambda row: (
                    int(row.get("level", 0) or 0),
                    int(row.get("score", 0) or 0)
                )
            )

            print("Existing best score:", best)

            return best

        except urllib.error.HTTPError as e:
            print("========================================")
            print("ERROR CHECKING PLAYER SCORE")
            print("HTTP status:", e.code)

            try:
                print(e.read().decode("utf-8"))
            except Exception:
                pass

            print("========================================")

            return None

        except Exception as e:
            print("========================================")
            print("ERROR CHECKING PLAYER SCORE")
            print(type(e).__name__, ":", e)
            print("========================================")

            return None

    # ============================================================
    # SUBMIT SCORE
    # ============================================================

    def submit_score(self, name, score, level):
        """
        Submits a player's score.

        Rules:

        - If the player has no previous score:
              INSERT a new row.

        - If the player already has a score:
              Update only if the new result is better.

        Ranking priority:
              1. Level
              2. Score

        The time column is a PostgreSQL timestamp.
        """

        print("")
        print("========================================")
        print("SUBMIT SCORE CALLED")
        print("Name:", name)
        print("Score:", score)
        print("Level:", level)
        print("========================================")

        # --------------------------------------------------------
        # Validate values
        # --------------------------------------------------------

        try:
            name = str(name).strip()
            score = int(score)
            level = int(level)
        except Exception as e:
            print("ERROR: Invalid score information.")
            print(e)
            return False

        if not name:
            print("ERROR: Player name is empty.")
            return False

        if score < 0:
            print("ERROR: Score cannot be negative.")
            return False

        if level < 1:
            print("ERROR: Level must be at least 1.")
            return False

        # --------------------------------------------------------
        # Get existing score
        # --------------------------------------------------------

        existing = self.get_player_score(name)

        # --------------------------------------------------------
        # Determine current time
        # --------------------------------------------------------

        current_time = datetime.now(timezone.utc).isoformat()

        print("Timestamp being sent:")
        print(current_time)

        # ========================================================
        # NO EXISTING SCORE -> INSERT
        # ========================================================

        if existing is None:

            print("")
            print("NO EXISTING SCORE.")
            print("Attempting INSERT...")
            print("")

            payload = {
                "name": name,
                "score": score,
                "level": level,
                "time": current_time
            }

            print("INSERT payload:")
            print(json.dumps(payload, indent=4))

            return self._insert_score(payload)

        # ========================================================
        # EXISTING SCORE -> CHECK IF BETTER
        # ========================================================

        old_level = int(existing.get("level", 0) or 0)
        old_score = int(existing.get("score", 0) or 0)

        print("")
        print("EXISTING SCORE FOUND")
        print("Old level:", old_level)
        print("Old score:", old_score)
        print("New level:", level)
        print("New score:", score)
        print("")

        new_is_better = False

        # Level is the primary ranking criterion.
        if level > old_level:
            new_is_better = True

        # If same level, score determines ranking.
        elif level == old_level and score > old_score:
            new_is_better = True

        if not new_is_better:
            print("New score is NOT better.")
            print("Keeping existing leaderboard entry.")
            print("========================================")
            return False

        # ========================================================
        # EXISTING SCORE -> UPDATE
        # ========================================================

        print("NEW SCORE IS BETTER.")
        print("Attempting UPDATE...")

        payload = {
            "name": name,
            "score": score,
            "level": level,
            "time": current_time
        }

        print("UPDATE payload:")
        print(json.dumps(payload, indent=4))

        return self._update_score(existing["id"], payload)

    # ============================================================
    # INSERT
    # ============================================================

    def _insert_score(self, payload):

        try:
            print("========================================")
            print("SUPABASE INSERT")
            print("========================================")

            body = json.dumps(payload).encode("utf-8")

            request = urllib.request.Request(
                self.base_url,
                data=body,
                headers=self._headers(include_content_type=True),
                method="POST"
            )

            print("Sending POST request...")

            with urllib.request.urlopen(request, timeout=10) as response:
                status = response.status
                raw_data = response.read().decode("utf-8")

            print("POST status:", status)
            print("POST response:", raw_data)

            # HTTP 2xx means success.
            if 200 <= status < 300:
                print("========================================")
                print("SUCCESS: SCORE INSERTED INTO SUPABASE")
                print("========================================")
                return True

            print("INSERT FAILED.")
            return False

        except urllib.error.HTTPError as e:

            print("========================================")
            print("SUPABASE INSERT HTTP ERROR")
            print("Status:", e.code)

            try:
                error_body = e.read().decode("utf-8")
                print("Supabase error:")
                print(error_body)
            except Exception:
                pass

            print("========================================")

            return False

        except urllib.error.URLError as e:

            print("========================================")
            print("SUPABASE INSERT URL ERROR")
            print(e)
            print("========================================")

            return False

        except Exception as e:

            print("========================================")
            print("SUPABASE INSERT ERROR")
            print(type(e).__name__, ":", e)
            print("========================================")

            return False

    # ============================================================
    # UPDATE
    # ============================================================

    def _update_score(self, row_id, payload):

        try:
            print("========================================")
            print("SUPABASE UPDATE")
            print("Row ID:", row_id)
            print("========================================")

            body = json.dumps(payload).encode("utf-8")

            params = urllib.parse.urlencode({
                "id": f"eq.{row_id}"
            })

            url = f"{self.base_url}?{params}"

            request = urllib.request.Request(
                url,
                data=body,
                headers=self._headers(include_content_type=True),
                method="PATCH"
            )

            print("Sending PATCH request...")
            print("URL:", url)

            with urllib.request.urlopen(request, timeout=10) as response:
                status = response.status
                raw_data = response.read().decode("utf-8")

            print("PATCH status:", status)
            print("PATCH response:", raw_data)

            if 200 <= status < 300:
                print("========================================")
                print("SUCCESS: SCORE UPDATED IN SUPABASE")
                print("========================================")
                return True

            print("UPDATE FAILED.")
            return False

        except urllib.error.HTTPError as e:

            print("========================================")
            print("SUPABASE UPDATE HTTP ERROR")
            print("Status:", e.code)

            try:
                error_body = e.read().decode("utf-8")
                print("Supabase error:")
                print(error_body)
            except Exception:
                pass

            print("========================================")

            return False

        except urllib.error.URLError as e:

            print("========================================")
            print("SUPABASE UPDATE URL ERROR")
            print(e)
            print("========================================")

            return False

        except Exception as e:

            print("========================================")
            print("SUPABASE UPDATE ERROR")
            print(type(e).__name__, ":", e)
            print("========================================")

            return False