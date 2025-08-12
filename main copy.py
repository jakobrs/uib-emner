import asyncio, aiohttp, sys
from bs4 import BeautifulSoup as BS
from types2 import *

url = "https://www4.uib.no/studier/emner"

rows = []

semaphore = asyncio.Semaphore(15)
i = 0
async def elab_course(session, code : str) -> Optional[Course1]:
    if "inf" not in code and "mat" not in code:
        return None

    global i
    i += 1
    if i % 20 == 0:
        print(i, code, file=sys.stderr)

    try:
        global semaphore, rows
        async with semaphore:
            async with session.get(f"{url}/{code}") as resp:
                bs = BS(await resp.text())
                headings = [
                    "studiepoeng",
                    "undervisningssemester",
                    "emnekode",
                    "talet på semester",
                    "undervisningsspråk",
                ]

                studiepoeng = semester = language = semester_count = None
                for e in bs.select("div:has(> dt)"):
                    body = e.find("dd").text
                    match e.find("dt").text:
                        case "Studiepoeng":
                            studiepoeng = float(body)
                        case "Undervisningssemester":
                            match body:
                                case "Haust":
                                    semester = "Høst"
                                case "Vår":
                                    semester = "Vår"
                                case "Haust, Vår":
                                    semester = "Høst, Vår"
                                case "Sommer":
                                    semester = "Sommer"
                                case _:
                                    print("idk what", body, "is")
                                    semester = body
                        case "Undervisningsspråk":
                            language = body
                        case "Talet på semester":
                            semester_count = int(body)

                mål = bs.select("div > h2 + div")
                if mål:
                    mål = mål[0]

                def get(name, k = lambda x: x):
                    a = bs.select(f"dt:contains({name}) + dd")
                    if a == []:
                        return None
                    else:
                        return k(a[0].text.strip())

                required = bs.select("summary:contains('Krav til forkunnskapar') + div")
                recommended = bs.select("summary:contains('Tilrådde forkunnskapar') + div")
                if required: required = required[0].text
                if recommended: recommended = recommended[0].text

                return Course1(
                    code = code,
                    title = bs.select("title")[0].text[:-6],
                    studiepoeng = studiepoeng,
                    semester = semester,
                    semester_count = semester_count,
                    language = language,
                    exam_type = get("Vurderingsordning"),
                    exam_date = get("Dato"),
                    exam_duration = get("Varigheit", lambda x: int(x[:-6])),
                    trekkfrist = get("Trekkfrist"),
                    required = required,
                    recommended = recommended,
                    department = bs.select(".text-balance")[0].text,
                    fulltime = None,
                    mål = str(mål),
                )
    except IndexError:
        print(code)
        raise

async def main():
    async with aiohttp.ClientSession() as session:
        courses = eval(open("out").read())
        data = await asyncio.gather(*(elab_course(session, row.code) for row in courses))

        print([row for row in data if row is not None])

asyncio.run(main())
