# Python Classroom

고등학생 대상 Python 수업을 GitHub Pages로 배포하기 위한 정적 학습 웹앱입니다.

## 구조

```text
.
├── index.html
├── lessons/
│   └── lesson-01.html
├── assets/
│   ├── styles.css
│   └── lesson-runner.js
├── tools/
│   └── generate_lesson.py
├── .codex/
│   └── skills/python-lesson-builder/
└── .github/
    └── workflows/pages.yml
```

## 로컬에서 보기

정적 HTML이라 `index.html`을 브라우저에서 열 수 있습니다. Pyodide CDN을 사용하므로
Python 실행기는 인터넷 연결이 있을 때 동작합니다.

## 새 차시 만들기

기본 1차시 HTML을 다시 생성하려면 저장소 루트에서 실행합니다.

```bash
python tools/generate_lesson.py --force
```

새 차시는 `lessons/data/lesson-02.json` 같은 콘텐츠 파일을 만든 뒤 생성합니다.

```bash
python tools/generate_lesson.py --content lessons/data/lesson-02.json
```

JSON에는 다음 필드가 필요합니다.

```json
{
  "number": 2,
  "title": "조건문",
  "summary": "조건에 따라 실행 흐름을 바꾸는 방법을 배웁니다.",
  "objectives": ["if문의 구조를 설명할 수 있다."],
  "concepts": [
    {
      "title": "조건문은 선택의 문장",
      "body": "조건이 참일 때만 특정 코드를 실행합니다."
    }
  ],
  "example_code": "score = 85\nif score >= 60:\n    print(\"통과\")",
  "practices": [
    {
      "title": "실습 1. 점수 판정하기",
      "body": "점수에 따라 통과 또는 재도전을 출력해 보세요."
    }
  ],
  "starter_code": "score = 85\nprint(score)"
}
```

차시를 추가한 뒤 `index.html`에 새 차시 링크를 추가합니다.

## Codex 스킬

프로젝트 로컬 스킬은 `.codex/skills/python-lesson-builder`에 있습니다. Codex에게
새 Python 차시를 만들거나 기존 차시를 다듬어 달라고 요청할 때 이 스킬이 같은
디자인 시스템과 생성기 사용 규칙을 안내합니다.

## GitHub Pages 배포

1. GitHub 저장소 Settings에서 Pages Source를 `GitHub Actions`로 설정합니다.
2. `main` 브랜치에 푸시합니다.
3. `.github/workflows/pages.yml`이 정적 파일을 GitHub Pages로 배포합니다.

원격 저장소 후보:

```bash
git remote add origin https://github.com/imuzikr/class-github-python.git
```
