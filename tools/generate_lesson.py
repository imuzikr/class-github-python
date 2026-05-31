#!/usr/bin/env python3
"""Generate a static Python lesson page for GitHub Pages."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from html import escape
from pathlib import Path
from textwrap import dedent


@dataclass(frozen=True)
class Practice:
    title: str
    body: str


@dataclass(frozen=True)
class Lesson:
    number: int
    title: str
    summary: str
    objectives: list[str]
    concepts: list[dict[str, str]]
    example_code: str
    practices: list[Practice]
    starter_code: str


DEFAULT_LESSON = Lesson(
    number=1,
    title="변수와 데이터",
    summary=(
        "Python에서 변수는 데이터를 저장하는 이름입니다. 이번 차시에서는 =로 "
        "값을 대입하고, 숫자가 들어 있는 변수로 계산하는 방법을 배웁니다."
    ),
    objectives=[
        "=가 값을 저장하는 대입 연산자임을 설명할 수 있다.",
        "같은 변수에 새 값을 대입하면 이전 값이 바뀐다는 것을 확인할 수 있다.",
        "숫자가 들어 있는 변수로 +, -, *, / 연산을 할 수 있다.",
        "숫자 데이터와 문자열 데이터의 쓰임을 구분할 수 있다.",
    ],
    concepts=[
        {
            "title": "=는 대입 연산자",
            "body": (
                "a = 3은 변수 a에 숫자 3을 저장한다는 뜻입니다. 수학의 같다와 달리 "
                "Python의 =는 오른쪽 값을 왼쪽 이름에 넣는 대입 연산자입니다."
            ),
        },
        {
            "title": "변수의 값은 다시 바뀔 수 있음",
            "body": (
                "a = 3 다음에 a = 5를 실행하면 a의 값은 5가 됩니다. 변수는 "
                "마지막으로 대입된 값을 기억합니다."
            ),
        },
        {
            "title": "a = a + 1의 원리",
            "body": (
                "a = a + 1은 먼저 오른쪽의 a + 1을 계산한 뒤, 그 결과를 다시 "
                "a에 저장합니다. 그래서 값이 1 증가합니다."
            ),
        },
        {
            "title": "숫자와 문자열 데이터",
            "body": (
                '숫자는 계산할 수 있고 문자열은 글자를 나타냅니다. score = 80은 '
                '계산 가능한 숫자, name = "민지"는 글자 데이터입니다.'
            ),
        },
    ],
    example_code=dedent(
        '''\
        a = 3
        print(a)

        a = 5
        print(a)

        a = a + 1
        print(a)

        score = 80
        print(score + 10)
        print(score - 5)
        print(score * 2)
        print(score / 4)

        name = "민지"
        print(name)
        '''
    ),
    practices=[
        Practice(
            "실습 1. 변수 값 바꾸기",
            "a = 3을 출력한 뒤, a = 5로 다시 대입하고 한 번 더 출력해 보세요. 어떤 값이 마지막에 남는지 확인합니다.",
        ),
        Practice(
            "실습 2. a = a + 1 실험하기",
            "a = a + 1을 여러 번 실행해 보세요. 오른쪽 값을 먼저 계산하고 다시 왼쪽 변수에 저장한다는 점을 확인합니다.",
        ),
        Practice(
            "실습 3. 숫자 변수로 계산하기",
            "score 또는 price 같은 숫자 변수를 만들고 +, -, *, / 연산 결과를 출력해 보세요.",
        ),
        Practice(
            "실습 4. 문자열 변수 만들기",
            'name = "민지"처럼 이름이나 과목명을 문자열 변수에 저장하고 출력해 보세요. 글자는 따옴표로 감쌉니다.',
        ),
    ],
    starter_code=dedent(
        '''\
        a = 3
        print(a)

        a = 5
        print(a)

        a = a + 1
        print(a)

        score = 80
        print(score + 10)

        name = "민지"
        print(name)
        '''
    ),
)


def load_lesson(path: Path | None) -> Lesson:
    if path is None:
        return DEFAULT_LESSON

    data = json.loads(path.read_text(encoding="utf-8"))
    return Lesson(
        number=int(data["number"]),
        title=str(data["title"]),
        summary=str(data["summary"]),
        objectives=[str(item) for item in data["objectives"]],
        concepts=[{"title": str(item["title"]), "body": str(item["body"])} for item in data["concepts"]],
        example_code=str(data["example_code"]),
        practices=[Practice(str(item["title"]), str(item["body"])) for item in data["practices"]],
        starter_code=str(data["starter_code"]),
    )


def render_list(items: list[str], class_name: str) -> str:
    lines = [f'          <li>{escape(item)}</li>' for item in items]
    return f'        <ul class="{class_name}">\n' + "\n".join(lines) + "\n        </ul>"


def render_concepts(concepts: list[dict[str, str]]) -> str:
    cards = []
    for concept in concepts:
        cards.append(
            dedent(
                f'''\
                <article class="concept-card">
                  <h3>{escape(concept["title"])}</h3>
                  <p>{escape(concept["body"])}</p>
                </article>'''
            )
        )
    return "\n".join(cards)


def render_practices(practices: list[Practice]) -> str:
    cards = []
    for index, practice in enumerate(practices):
        current = ' aria-current="true"' if index == 0 else ""
        cards.append(
            dedent(
                f'''\
                <article class="practice-question"{current}>
                  <h3>{escape(practice.title)}</h3>
                  <p>{escape(practice.body)}</p>
                </article>'''
            )
        )
    return "\n".join(cards)


def render_lesson(lesson: Lesson) -> str:
    lesson_id = f"{lesson.number:02d}"
    return dedent(
        f'''\
        <!doctype html>
        <html lang="ko">
          <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>{lesson.number}차시 {escape(lesson.title)} | Python Classroom</title>
            <meta name="description" content="고등학생을 위한 Python {lesson.number}차시: {escape(lesson.title)}">
            <link rel="stylesheet" href="../assets/styles.css">
            <script defer src="https://cdn.jsdelivr.net/pyodide/v0.26.4/full/pyodide.js"></script>
            <script defer src="../assets/lesson-runner.js"></script>
          </head>
          <body>
            <header class="site-header">
              <nav class="nav-shell" aria-label="주요 메뉴">
                <a class="brand" href="../index.html">
                  <span class="brand-mark" aria-hidden="true">Py</span>
                  <span>
                    <strong>Python Classroom</strong>
                    <small>{lesson.number}차시 {escape(lesson.title)}</small>
                  </span>
                </a>
                <a class="nav-link" href="../index.html">차시 목록</a>
              </nav>
            </header>

            <main>
              <section class="lesson-hero">
                <div class="lesson-hero-inner">
                  <p class="eyebrow">Lesson {lesson_id}</p>
                  <h1>{escape(lesson.title)}</h1>
                  <p>{escape(lesson.summary)}</p>
        {render_list(lesson.objectives, "objective-list")}
                </div>
              </section>

              <section class="section">
                <div class="section-heading">
                  <p class="eyebrow">Concept</p>
                  <h2>기본 개념</h2>
                </div>
                <div class="concept-grid">
        {render_concepts(lesson.concepts)}
                </div>
              </section>

              <section class="section">
                <div class="section-heading">
                  <p class="eyebrow">Example</p>
                  <h2>예제 코드</h2>
                </div>
                <pre class="code-block"><code>{escape(lesson.example_code.strip())}</code></pre>
              </section>

              <section class="section" id="practice">
                <div class="section-heading">
                  <p class="eyebrow">Practice</p>
                  <h2>직접 실습하기</h2>
                </div>

                <div class="practice-layout">
                  <div class="practice-stack" aria-label="실습 질문">
        {render_practices(lesson.practices)}
                    <aside class="note-panel">
                      <h3>체크리스트</h3>
                      <ul class="check-list">
                        <li>변수 이름과 코드의 의미를 설명할 수 있나요?</li>
                        <li>실행 결과와 오류 메시지를 읽어 보았나요?</li>
                        <li>예제에서 한 가지 이상을 바꾸어 다시 실행했나요?</li>
                      </ul>
                    </aside>
                  </div>

                  <section class="runner-panel" aria-label="Python 코드 실행기">
                    <div class="runner-toolbar">
                      <span class="runner-status" data-runner-status>Python 준비 중</span>
                      <button class="button button-primary" type="button" data-run-python disabled>실행</button>
                    </div>
                    <label class="visually-hidden" for="python-code">Python 코드 입력</label>
                    <textarea
                      id="python-code"
                      class="code-editor"
                      spellcheck="false"
                      data-python-editor
                      placeholder="왼쪽 실습 질문을 보고 직접 코드를 입력해 보세요.\n\n예)\n{escape(lesson.starter_code.strip())}"
                    ></textarea>
                    <div class="output-shell">
                      <span class="output-label">입력 결과</span>
                      <pre class="output-panel" aria-live="polite" data-python-output>코드를 직접 입력한 뒤 실행 버튼을 눌러 보세요.</pre>
                      <div class="explanation-panel" data-error-explanation hidden></div>
                    </div>
                  </section>
                </div>
              </section>
            </main>
          </body>
        </html>
        '''
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a Python lesson HTML page.")
    parser.add_argument("--content", type=Path, help="Optional lesson JSON content file.")
    parser.add_argument("--out-dir", type=Path, default=Path("lessons"), help="Output directory.")
    parser.add_argument("--force", action="store_true", help="Overwrite an existing lesson file.")
    args = parser.parse_args()

    lesson = load_lesson(args.content)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    output_path = args.out_dir / f"lesson-{lesson.number:02d}.html"

    if output_path.exists() and not args.force:
        raise SystemExit(f"{output_path} already exists. Re-run with --force to overwrite it.")

    output_path.write_text(render_lesson(lesson), encoding="utf-8")
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
