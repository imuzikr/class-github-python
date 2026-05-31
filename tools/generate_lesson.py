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
    title="변수와 자료형",
    summary=(
        "Python에서 변수는 값을 담는 이름표입니다. 이번 차시에서는 값을 변수에 "
        "저장하고, 저장된 값이 어떤 자료형인지 직접 확인합니다."
    ),
    objectives=[
        "변수에 값을 저장하는 문법을 설명할 수 있다.",
        "정수, 실수, 문자열, 불리언 자료형을 구분할 수 있다.",
        "type()으로 값의 자료형을 확인할 수 있다.",
    ],
    concepts=[
        {
            "title": "변수는 값을 저장하는 이름",
            "body": (
                'name = "민지"처럼 왼쪽에는 변수 이름, 오른쪽에는 저장할 값을 씁니다. '
                "등호는 같다라는 뜻이 아니라 값을 넣는다는 뜻으로 읽습니다."
            ),
        },
        {
            "title": "자료형은 값의 종류",
            "body": (
                "Python은 값의 종류를 자료형으로 구분합니다. 대표적으로 정수 int, "
                "실수 float, 문자열 str, 불리언 bool이 있습니다."
            ),
        },
    ],
    example_code=dedent(
        '''\
        name = "민지"
        age = 17
        height = 162.5
        is_student = True

        print(name)
        print(type(age))
        print(type(height))
        print(type(is_student))
        '''
    ),
    practices=[
        Practice(
            "실습 1. 나를 소개하는 변수 만들기",
            "student_name, grade, favorite_subject 변수를 만들고 print()로 출력해 보세요.",
        ),
        Practice(
            "실습 2. 자료형 확인하기",
            "각 변수 아래에 type()을 사용한 출력문을 추가해서 값의 자료형을 확인해 보세요.",
        ),
        Practice(
            "실습 3. 오류 고치기",
            "숫자와 문자열을 연결하다가 오류가 생기면 str()로 숫자를 문자열로 바꾸어 해결할 수 있습니다.",
        ),
    ],
    starter_code=dedent(
        '''\
        student_name = "민지"
        grade = 2
        favorite_subject = "정보"

        print("이름:", student_name)
        print("학년:", grade)
        print("좋아하는 과목:", favorite_subject)

        print(type(student_name))
        print(type(grade))
        print(type(favorite_subject))
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
