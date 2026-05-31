(function () {
  const editor = document.querySelector("[data-python-editor]");
  const output = document.querySelector("[data-python-output]");
  const explanation = document.querySelector("[data-error-explanation]");
  const runButton = document.querySelector("[data-run-python]");
  const status = document.querySelector("[data-runner-status]");
  const practiceTabs = document.querySelectorAll("[data-practice-tab]");
  const practicePanels = document.querySelectorAll("[data-practice-panel]");

  if (!editor || !output || !runButton || !status || !explanation) {
    return;
  }

  let pyodideReadyPromise = null;

  function selectPractice(panelId) {
    practiceTabs.forEach((tab) => {
      tab.setAttribute("aria-selected", String(tab.dataset.practiceTab === panelId));
    });

    practicePanels.forEach((panel) => {
      const isActive = panel.id === panelId;
      panel.hidden = !isActive;
      panel.setAttribute("aria-current", String(isActive));
    });
  }

  function setStatus(message) {
    status.textContent = message;
  }

  function setOutput(message, isError) {
    output.textContent = message;
    output.classList.toggle("error", Boolean(isError));
  }

  function setExplanation(title, message, isVisible) {
    explanation.hidden = !isVisible;
    explanation.innerHTML = "";

    if (!isVisible) {
      return;
    }

    const heading = document.createElement("strong");
    heading.textContent = title;
    const body = document.createElement("span");
    body.textContent = message;
    explanation.append(heading, body);
  }

  function explainPythonError(message) {
    if (message.includes("NameError")) {
      return "사용한 변수 이름이 아직 만들어지지 않았을 가능성이 큽니다. 변수 이름의 철자가 같은지, 값을 먼저 저장한 뒤 사용했는지 확인해 보세요.";
    }

    if (message.includes("SyntaxError")) {
      if (message.includes("unterminated string literal") || message.includes("EOL while scanning string literal")) {
        return "문자열의 따옴표가 닫히지 않았습니다. 글자를 따옴표로 감쌌다면 시작 따옴표와 끝 따옴표가 짝을 이루는지 확인해 보세요.";
      }
      return "Python 문법에 맞지 않는 부분이 있습니다. 괄호, 따옴표, 쉼표, 등호의 위치를 천천히 확인해 보세요.";
    }

    if (message.includes("TypeError")) {
      return "숫자와 글자를 같은 방식으로 계산하려고 했을 가능성이 큽니다. 이번 차시에서는 숫자는 숫자끼리 +, -, *, /로 계산하고, 글자는 따옴표로 감싸 출력해 보세요.";
    }

    if (message.includes("IndentationError")) {
      return "들여쓰기 칸 수가 맞지 않습니다. 같은 코드 블록 안의 문장들은 같은 칸만큼 들여쓰기해야 합니다.";
    }

    if (message.includes("ZeroDivisionError")) {
      return "숫자를 0으로 나누려고 했습니다. 나누는 값이 0이 아닌지 확인해 보세요.";
    }

    return "오류 메시지의 마지막 줄을 먼저 읽어 보세요. 어떤 줄에서 문제가 생겼는지 확인한 뒤 변수 이름, 따옴표, 괄호, 숫자와 문자열 사용을 차례로 점검하면 좋습니다.";
  }

  async function loadRuntime() {
    if (!pyodideReadyPromise) {
      runButton.disabled = true;
      setStatus("Python 준비 중");
      pyodideReadyPromise = loadPyodide({
        stdout: (text) => {
          output.textContent += `${text}\n`;
        },
        stderr: (text) => {
          output.textContent += `${text}\n`;
        },
      });
    }

    const pyodide = await pyodideReadyPromise;
    setStatus("Python 준비 완료");
    runButton.disabled = false;
    return pyodide;
  }

  async function runCode() {
    const pyodide = await loadRuntime();
    const code = editor.value.trim();

    if (!code) {
      setOutput("아직 입력한 코드가 없습니다. 왼쪽 실습 질문을 보고 Python 코드를 작성해 보세요.", false);
      setExplanation("입력 안내", "먼저 a = 3처럼 변수에 값을 대입하고, print(a)로 출력하는 코드를 직접 작성해 보세요.", true);
      return;
    }

    runButton.disabled = true;
    setStatus("실행 중");
    setOutput("", false);
    setExplanation("", "", false);

    try {
      await pyodide.runPythonAsync(code);
      if (!output.textContent.trim()) {
        setOutput("출력된 내용이 없습니다. print()를 사용해 결과를 확인해 보세요.", false);
        setExplanation("결과 안내", "변수에 값을 저장하는 것만으로는 화면에 보이지 않습니다. 결과를 확인하려면 print(변수이름)을 추가해 보세요.", true);
      }
      setStatus("실행 완료");
    } catch (error) {
      const message = error && error.message ? error.message : String(error);
      setOutput(`오류가 발생했습니다.\n\n${message}`, true);
      setExplanation("오류 원인 힌트", explainPythonError(message), true);
      setStatus("오류 확인 필요");
    } finally {
      runButton.disabled = false;
    }
  }

  editor.addEventListener("keydown", (event) => {
    if (event.key === "Tab") {
      event.preventDefault();
      const start = editor.selectionStart;
      const end = editor.selectionEnd;
      editor.value = `${editor.value.slice(0, start)}    ${editor.value.slice(end)}`;
      editor.selectionStart = start + 4;
      editor.selectionEnd = start + 4;
    }
  });

  practiceTabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      selectPractice(tab.dataset.practiceTab);
    });
  });

  runButton.addEventListener("click", runCode);
  loadRuntime().catch((error) => {
    setOutput(`Python 실행 환경을 불러오지 못했습니다.\n\n${error.message || error}`, true);
    setExplanation("초기화 오류", "인터넷 연결 또는 Pyodide CDN 로딩 상태를 확인해 보세요.", true);
    setStatus("초기화 실패");
  });
})();
