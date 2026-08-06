import asyncio
import json
import urllib.request
import urllib.parse
import urllib.error

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

        # Diagnostic fields to help identify issues during development
        self.last_status = None
        self.last_response = None
        self.last_error = None





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
                headers["Prefer"] = "return=representation"

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

                print("SUPABASE STATUS:", status)

                if raw:
                    try:
                        parsed = json.loads(raw)
                    except Exception:
                        parsed = raw

                    self.last_response = parsed
                    return parsed

                self.last_response = None
                return []

        except urllib.error.HTTPError as he:
            try:
                body = he.read().decode("utf-8")
            except Exception:
                body = None

            error_text = f"HTTP {he.code}: {body}"
            print("SUPABASE HTTP ERROR:", error_text)
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
            name
        )



        existing = await self.request(

            "GET",

            params=f"?name=eq.{safe_name}"

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

        if self.last_status and 200 <= int(self.last_status) < 300:
            return True

        if self.last_error is not None:
            print(f"SUBMIT FAILED: {self.last_error}")
            return False

        # If no status and no error, assume submission may have succeeded but we do not have a response.
        print("SUBMIT WARNING: no HTTP status available; submission may have been sent but response was empty")
        return True






    async def get_top_scores(self):

        print(
            "GET TOP SCORES"
        )



        scores = await self.request(

            "GET",

            params=
            "?order=level.desc,score.desc&limit=10"

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

            params=
            "?order=level.desc,score.desc"

        )



        for index, player in enumerate(

            players,

            start=1

        ):



            if player.get(
                "name"
            ) == name:



                return index, player




        return None, None