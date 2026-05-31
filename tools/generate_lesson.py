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
            "title": "숫자형 데이터는 계산 가능한 값으로 저장됨",
            "body": (
                "score = 80을 실행하면 Python은 80을 계산할 수 있는 숫자 데이터로 "
                "보고, 그 값을 score라는 이름에 저장합니다. 그래서 score + 10처럼 "
                "바로 계산할 수 있습니다."
            ),
        },
        {
            "title": "문자열 데이터는 따옴표로 감싼 글자로 저장됨",
            "body": (
                'name = "민지"를 실행하면 Python은 따옴표 안의 민지를 글자 '
                "데이터로 보고 name에 저장합니다. 따옴표가 없으면 Python은 "
                "글자가 아니라 이미 만들어진 변수 이름을 찾으려고 합니다."
            ),
        },
        {
            "title": "=는 오른쪽 값을 왼쪽 변수에 넣는 대입",
            "body": (
                "a = 3은 a와 3이 같다는 뜻이 아니라, 오른쪽의 3을 왼쪽 변수 "
                "a에 저장한다는 뜻입니다. Python은 항상 오른쪽을 먼저 읽습니다."
            ),
        },
        {
            "title": "같은 변수에 다시 대입하면 저장된 값이 바뀜",
            "body": (
                "a = 3 다음에 a = 5를 실행하면 a는 마지막에 저장한 5를 기억합니다. "
                "a = a + 1은 기존 a를 읽고 1을 더한 뒤, 그 결과를 다시 a에 저장합니다."
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
            "숫자형 데이터를 변수에 저장하기",
            "score = 80처럼 숫자를 따옴표 없이 변수에 저장하고, print(score)로 출력해 보세요. 숫자는 계산 가능한 값으로 저장됩니다.",
        ),
        Practice(
            "문자열 데이터를 변수에 저장하기",
            'name = "민지"처럼 글자는 따옴표로 감싸서 저장합니다. 따옴표를 지우면 Python이 변수 이름을 찾으려 한다는 점도 실험해 보세요.',
        ),
        Practice(
            "변수 값 바꾸기",
            "a = 3을 출력한 뒤 a = 5를 다시 대입하고 출력해 보세요. 변수에는 마지막으로 대입한 값이 남습니다.",
        ),
        Practice(
            "a = a + 1 원리 확인하기",
            "a = a + 1을 여러 번 실행해 보세요. 오른쪽 값을 먼저 계산하고 그 결과를 다시 왼쪽 변수에 저장하는 흐름을 출력 결과로 확인합니다.",
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
        number = index + 1
        active_class = " is-active" if index == 0 else ""
        current = "true" if index == 0 else "false"
        hidden = "false" if index == 0 else "true"
        cards.append(
            dedent(
                f'''\
                <article class="practice-question{active_class}" id="practice-{number}" role="tabpanel" aria-current="{current}" aria-hidden="{hidden}" data-practice-panel>
                  <p class="lesson-meta">실습 {number}</p>
                  <h3>{escape(practice.title)}</h3>
                  <p>{escape(practice.body)}</p>
                </article>'''
            )
        )
    return "\n".join(cards)


def render_lesson(lesson: Lesson) -> str:
    lesson_id = f"{lesson.number:02d}"
    practice_tab_lines = []
    for index, practice in enumerate(lesson.practices):
        number = index + 1
        active_class = " is-active" if index == 0 else ""
        selected = str(index == 0).lower()
        practice_tab_lines.extend(
            [
                f'                      <button class="practice-tab{active_class}" type="button" role="tab" aria-selected="{selected}" aria-controls="practice-{number}" data-practice-tab="practice-{number}">',
                f"                        <span>{number}</span>",
                f"                        <strong>{escape(practice.title)}</strong>",
                "                      </button>",
            ]
        )
    practice_tabs = "\n".join(practice_tab_lines)
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
                  <div class="lesson-hero-copy">
                    <p class="eyebrow">Lesson {lesson_id}</p>
                    <h1>{escape(lesson.title)}</h1>
                    <p>{escape(lesson.summary)}</p>
        {render_list(lesson.objectives, "objective-list")}
                  </div>
                  <aside class="lesson-hero-panel" aria-label="실습 흐름 미리보기">
                    <p class="panel-kicker">Practice Flow</p>
                    <div class="flow-row">
                      <code>1. 읽기</code>
                      <span>개념과 예제 코드를 먼저 확인합니다.</span>
                    </div>
                    <div class="flow-row">
                      <code>2. 입력하기</code>
                      <span>오른쪽 입력창에 직접 Python 코드를 작성합니다.</span>
                    </div>
                    <div class="flow-row">
                      <code>3. 실행하기</code>
                      <span>결과와 오류 힌트를 보며 코드를 고칩니다.</span>
                    </div>
                  </aside>
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
                  <section class="practice-card" aria-label="실습 과제">
                    <div class="practice-tabs" role="tablist" aria-label="실습 선택">
        {practice_tabs}
                    </div>
        {render_practices(lesson.practices)}
                    <aside class="note-panel">
                      <h3>체크리스트</h3>
                      <ul class="check-list">
                        <li>=를 같다 대신 대입으로 읽었나요?</li>
                        <li>숫자 데이터는 따옴표 없이 저장했나요?</li>
                        <li>문자열 데이터는 따옴표로 감쌌나요?</li>
                        <li>실행 결과와 오류 메시지를 읽어 보았나요?</li>
                      </ul>
                    </aside>
                  </section>

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
