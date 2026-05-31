(function () {
  const editor = document.querySelector("[data-python-editor]");
  const output = document.querySelector("[data-python-output]");
  const runButton = document.querySelector("[data-run-python]");
  const status = document.querySelector("[data-runner-status]");

  if (!editor || !output || !runButton || !status) {
    return;
  }

  let pyodideReadyPromise = null;

  function setStatus(message) {
    status.textContent = message;
  }

  function setOutput(message, isError) {
    output.textContent = message;
    output.classList.toggle("error", Boolean(isError));
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
    runButton.disabled = true;
    setStatus("실행 중");
    setOutput("", false);

    try {
      await pyodide.runPythonAsync(editor.value);
      if (!output.textContent.trim()) {
        setOutput("출력된 내용이 없습니다. print()를 사용해 결과를 확인해 보세요.", false);
      }
      setStatus("실행 완료");
    } catch (error) {
      const message = error && error.message ? error.message : String(error);
      setOutput(`오류가 발생했습니다.\n\n${message}`, true);
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

  runButton.addEventListener("click", runCode);
  loadRuntime().catch((error) => {
    setOutput(`Python 실행 환경을 불러오지 못했습니다.\n\n${error.message || error}`, true);
    setStatus("초기화 실패");
  });
})();
