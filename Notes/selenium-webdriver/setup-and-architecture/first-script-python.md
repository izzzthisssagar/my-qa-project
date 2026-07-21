---
title: "Your first Selenium script in Python"
tags: ["selenium-webdriver", "setup-and-architecture", "python", "track-d"]
updated: "2026-07-18"
---

# Your first Selenium script in Python

*Create an isolated environment, install Selenium through the same interpreter that runs the script, assert the official web form, and prove cleanup survives failure.*

> `pip install selenium` can succeed perfectly and your import can still fail. Python packages belong
> to interpreters, not vaguely to "the computer." Your first script is therefore two tests before it
> is a browser test: prove which Python is running, then prove Selenium was installed for that exact
> Python. Only then open Chrome, assert behaviour, and close it even after failure.

> **In real life**
>
> A diagnostic laboratory has separate benches. Reagents stocked at the bench labelled system Python
> do not magically appear at the isolated `.venv` bench, even if both benches are in the same room.
> `python3 -m pip` is a delivery label: it sends Selenium to the interpreter named before `-m`. The
> session is the experiment, the assertion is the result, and `finally` is the mandatory shutdown.

**virtual environment**: A Python virtual environment is an isolated directory containing a specific Python interpreter context and its own site-packages. Activation changes command lookup, but sys.executable is the direct evidence of which interpreter is actually running a script.

## Bind installation and execution to one interpreter

On macOS or Linux, start in the project directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install selenium
python3 -c "import sys, selenium; print(sys.executable); print(selenium.__version__)"
```

On Windows PowerShell, activate with `.venv\Scripts\Activate.ps1`. Using `python3 -m pip` is safer
than a bare `pip` because the interpreter is explicit. `sys.executable` then proves what will run the
script. Modern Selenium can manage a suitable driver automatically, but it cannot import a package
installed into a different Python environment.

> **Tip**
>
> When `import selenium` fails, run the import check with the exact command used to start the test:
> `python3 -c "import sys; print(sys.executable)"` followed by `python3 -m pip show selenium`. Matching
> the command prefix matters more than whether the prompt displays `(.venv)`.

> **Common mistake**
>
> Running `pip install selenium`, seeing "Requirement already satisfied," and assuming every Python
> can import it. That message only describes the pip executable you invoked. It says nothing about a
> different interpreter selected by an IDE, shell alias, CI runner, or notebook kernel.

![A hospital laboratory desk with pipettes, racks of tubes, instruments, and distinct work areas arranged across the bench](first-script-python.jpg)
*Laboratory desk — Luca Volpi (Goldmund100), CC BY-SA 3.0. [Source](https://commons.wikimedia.org/wiki/File:Laboratory_desk.jpg)*
- **Pipettes = python -m pip** — A delivery instrument belongs to a specific workflow. Naming Python before -m pip ties package installation to that interpreter.
- **Blue tip rack = isolated environment** — The separated rack holds its own supplies. A virtual environment similarly owns a package location; packages on another bench are unavailable.
- **Tube labels = runtime evidence** — Labels identify which sample is actually being processed. sys.executable identifies the interpreter, and python -m pip identifies its package inventory.
- **Ordered tube rack = assertion and cleanup** — A controlled workflow records results and disposes of work safely. Explicit assertions judge browser state, while finally guarantees driver.quit after success or failure.

**From isolated Python to a cleaned-up browser**

1. **Create and select .venv** — The project gets an isolated package context; activation makes its interpreter the shell default.
2. **Install through that Python** — python3 -m pip install selenium binds installation to the named interpreter.
3. **Verify identity and import** — sys.executable and selenium.__version__ provide direct runtime evidence.
4. **Start, navigate, interact, assert** — webdriver.Chrome creates a session; the test compares title and submitted message.
5. **Quit from finally** — The browser closes whether the assertion passes, fails, or another command raises.

## The real Selenium path

Prerequisites: Python 3, an active project environment containing Selenium, Chrome, and network
access to the official test page (and possibly for first-run driver management). This fenced example
uses the real Selenium API; the later playgrounds deliberately do not.

```python
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
try:
    driver.get("https://www.selenium.dev/selenium/web/web-form.html")
    assert driver.title == "Web form", f"unexpected title: {driver.title!r}"

    driver.find_element(By.NAME, "my-text").send_keys("Selenium")
    driver.find_element(By.CSS_SELECTOR, "button").click()

    message = driver.find_element(By.ID, "message").text
    assert message == "Received!", f"unexpected message: {message!r}"
finally:
    driver.quit()
```

The playgrounds are **standard-library simulations**, not Selenium. They model interpreter/package
resolution and teardown after an assertion failure without a browser, driver, package, or network.

*Prove environment matching and cleanup after failure — Python*

```python
runtime = "/venv/bin/python"
first_installed_for = "/usr/bin/python"
corrected_installed_for = "/venv/bin/python"
events = []

def package_matches(interpreter, installed_for):
    return interpreter == installed_for

mismatch_detected = not package_matches(runtime, first_installed_for)
corrected = package_matches(runtime, corrected_installed_for)
teardown_after_failure = False

print(f"RUNTIME interpreter={runtime}")
print(f"RESOLVE installed={first_installed_for} MISMATCH_REJECTED")
print(f"RESOLVE installed={corrected_installed_for} CORRECTED")

events.append("START session=session-7")
try:
    events.append("ASSERT simulated=FAIL")
    raise AssertionError("simulated assertion failure")
except AssertionError:
    pass
finally:
    events.append("QUIT session=session-7")
    teardown_after_failure = events[-1].startswith("QUIT ")

assert mismatch_detected, "mismatched package location was accepted"
assert corrected, "corrected package location was rejected"
assert teardown_after_failure, "finally did not record cleanup"

for event in events:
    print(event)
print(f"RESULT mismatch_detected={str(mismatch_detected).lower()} corrected={str(corrected).lower()} teardown_after_failure={str(teardown_after_failure).lower()}")
```

*Model the equivalent runtime/dependency boundary — Java*

```java
import java.util.ArrayList;
import java.util.List;

public class Main {
    static boolean packageMatches(String runtime, String installedFor) {
        return runtime.equals(installedFor);
    }

    public static void main(String[] args) {
        String runtime = "/venv/bin/python";
        String firstInstalledFor = "/usr/bin/python";
        String correctedInstalledFor = "/venv/bin/python";
        List<String> events = new ArrayList<>();

        boolean mismatchDetected = !packageMatches(runtime, firstInstalledFor);
        boolean corrected = packageMatches(runtime, correctedInstalledFor);
        boolean teardownAfterFailure = false;

        System.out.println("RUNTIME interpreter=" + runtime);
        System.out.println("RESOLVE installed=" + firstInstalledFor + " MISMATCH_REJECTED");
        System.out.println("RESOLVE installed=" + correctedInstalledFor + " CORRECTED");

        events.add("START session=session-7");
        try {
            events.add("ASSERT simulated=FAIL");
            throw new AssertionError("simulated assertion failure");
        } catch (AssertionError expected) {
            // The oracle continues so it can inspect finally cleanup.
        } finally {
            events.add("QUIT session=session-7");
            teardownAfterFailure = events.get(events.size() - 1).startsWith("QUIT ");
        }

        if (!mismatchDetected) throw new AssertionError("mismatched package location was accepted");
        if (!corrected) throw new AssertionError("corrected package location was rejected");
        if (!teardownAfterFailure) throw new AssertionError("finally did not record cleanup");

        events.forEach(System.out::println);
        System.out.println("RESULT mismatch_detected=" + mismatchDetected + " corrected=" + corrected + " teardown_after_failure=" + teardownAfterFailure);
    }
}
```

### Your first time: Run the real script from a known environment

- [ ] Create a project environment — Run python3 -m venv .venv and activate it for your shell.
- [ ] Install through the intended interpreter — Use python3 -m pip install selenium, not an unqualified pip command.
- [ ] Capture interpreter evidence — Print sys.executable and selenium.__version__ with the same Python command used for the script.
- [ ] Run and inspect assertions — The script should verify both Web form and Received!, not just interact.
- [ ] Force failure and inspect cleanup — Change one expected value, rerun, and verify Chrome still closes.

- **ModuleNotFoundError: No module named 'selenium'**
  Print sys.executable with the command that failed, then run that same interpreter with -m pip show selenium. Install into that environment or configure the runner to use the intended .venv interpreter.
- **pip says Selenium is installed but import still fails**
  Bare pip and the running Python point to different environments. Compare their paths and repeat installation as python3 -m pip install selenium using the exact runtime command.
- **The terminal works but the IDE or CI fails**
  The IDE interpreter, notebook kernel, or CI executable differs from the activated shell. Inspect sys.executable inside the failing context and select or provision the same environment there.
- **Chrome remains after an assertion error**
  Cleanup is after the assertion rather than in finally. Wrap all session work in try and call driver.quit() in finally.
- **The script stays green when the page is wrong**
  Clicks and typing are actions only. Compare title or result text with an explicit expected value so wrong behaviour raises.

### Where to check

- **`sys.executable`** — direct evidence of the interpreter running this process.
- **`python3 -m pip show selenium`** — package evidence tied to that Python command.
- **IDE interpreter or notebook kernel settings** — often different from the activated terminal.
- **CI command and PATH** — the runner may select a system Python rather than `.venv`.
- **Task Manager or Activity Monitor** — confirmation that a forced assertion failure still cleans up.

### Worked example: Requirement already satisfied — for somebody else's Python

Arun activates `.venv` but his editor still runs `/usr/bin/python`. In the terminal, a bare `pip`
reports Selenium installed; the editor raises `ModuleNotFoundError`. He prints `sys.executable` from
the editor task and sees the system path. Rather than reinstall everywhere, he selects
`.venv/bin/python`, runs that interpreter with `-m pip show selenium`, and reruns. The browser now
starts. He deliberately fails the message assertion and confirms `finally` still closes Chrome,
proving environment selection and lifecycle independently.

**Quiz.** pip reports Selenium installed, but the script raises ModuleNotFoundError. Which evidence should you collect first?

- [ ] The installed Chrome version only
- [x] sys.executable from the failing run and pip show invoked through that exact Python
- [ ] A screenshot of the activated prompt
- [ ] The web page title

*The error occurs before browser startup. sys.executable identifies the runtime, and that runtime's -m pip shows whether Selenium exists in its package location. Prompt decoration is indirect evidence; Chrome and page state are not involved yet.*

- **Why use python3 -m pip?** — It ties pip execution to the explicitly named Python interpreter.
- **Best interpreter evidence** — sys.executable printed inside the same context that runs the test.
- **What does activation do?** — It prepends the environment's executable directory to command lookup; it is useful but not stronger evidence than sys.executable.
- **Why assert after interaction?** — Typing and clicking prove only that commands ran; an assertion proves the expected browser state resulted.
- **Why quit in finally?** — An exception can interrupt the happy path, while finally still ends the session.

### Challenge

Run the import check from both your system Python and `.venv` Python and record the two
`sys.executable` values. Then run the real example, deliberately break the expected message, and
prove Chrome closes. Explain why environment identity and teardown are separate oracles.

### Ask the community

> My Python first script fails at [import / session start / assertion / teardown]. Here are sys.executable, python -m pip show selenium, the first error, and whether Chrome remains after failure. Which boundary is responsible?

Include evidence from the failing execution context. An activated prompt alone cannot prove which
interpreter an IDE, notebook, or CI runner selected.

- [Python documentation — venv](https://docs.python.org/3/library/venv.html)
- [Selenium — Install a Selenium library](https://www.selenium.dev/documentation/webdriver/getting_started/install_library/)
- [Selenium — Write your first Selenium script](https://www.selenium.dev/documentation/webdriver/getting_started/first_script/)
- [Selenium Python API documentation](https://www.selenium.dev/selenium/docs/api/py/index.html)

The first Selenium script begins around 3:18 in this broader beginner walkthrough.

🎬 [Selenium Tutorial for Beginners using Python | Selenium for Web Scraping (With Project)](https://www.youtube.com/watch?v=XI5_nsClCYI) (37 min)

- Python packages belong to specific interpreter environments; successful installation elsewhere does not satisfy this runtime.
- python3 -m pip and sys.executable provide direct, matching installation and execution evidence.
- webdriver.Chrome starts the same WebDriver session concept Java uses; the language tooling boundary is what differs.
- Actions need explicit assertions, and driver.quit() belongs in finally so failures cannot leak processes.
- The fenced example uses real Selenium; the playground pair is a deterministic standard-library model of environment resolution and cleanup.


## Related notes

- [[Notes/a-first-language-deeper/setup-and-ide/installing-python|Installing Python]]
- [[Notes/selenium-webdriver/setup-and-architecture/drivers-and-selenium-manager|Drivers & Selenium Manager]]
- [[Notes/selenium-webdriver/setup-and-architecture/first-script-java|First script (Java)]]


---
_Source: `packages/curriculum/content/notes/selenium-webdriver/setup-and-architecture/first-script-python.mdx`_
