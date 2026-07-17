# Processes

`subprocess` is the portable, idiomatic way to launch and communicate with
external programs. `os.fork()`/`os.exec*()` are the POSIX-only primitives
that `subprocess` itself is built on.

## subprocess.run: the common case

```python
import subprocess

result = subprocess.run(
    ["ls", "-la"],
    capture_output=True,
    text=True,          # decode stdout/stderr as str, not bytes
    check=True,          # raise CalledProcessError on non-zero exit
)
result.stdout, result.returncode
```

Passing a list (`["ls", "-la"]`) instead of a shell string avoids shell
injection entirely — arguments are passed directly to the OS's exec call,
never interpreted by a shell. Only pass `shell=True` with a string when you
specifically need shell features (globbing, pipes), and never with
untrusted input.

## Piping between processes

```python
p1 = subprocess.Popen(["cat", "file.txt"], stdout=subprocess.PIPE)
p2 = subprocess.run(["grep", "error"], stdin=p1.stdout, capture_output=True, text=True)
p1.stdout.close()   # lets p1 receive SIGPIPE if p2 exits early -- avoids a hang
```

## Handling failures

```python
result = subprocess.run(["false"])       # doesn't raise by default
result.returncode                          # 1

try:
    subprocess.run(["false"], check=True)
except subprocess.CalledProcessError as e:
    print(f"failed with code {e.returncode}")

subprocess.run(["sleep", "10"], timeout=2)   # raises TimeoutExpired after 2s
```

## os.fork()/os.exec*(): the low-level, POSIX-only mechanism

```python
import os

pid = os.fork()
if pid == 0:
    # Child: a near-exact copy of the parent's memory at the moment of fork()
    os.execvp("ls", ["ls", "-la"])   # replaces this process's image entirely
else:
    # Parent: pid is the child's process ID
    _, status = os.waitpid(pid, 0)
    print(os.WEXITSTATUS(status))
```

`fork()` duplicates the calling process; `exec*()` replaces the current
process image with a new program. `subprocess` combines these (or uses
`posix_spawn` where available) so you rarely need to call them directly —
this topic exists mainly to explain what `subprocess` does under the hood.

## Common pitfalls

| Pitfall | Consequence | Fix |
|---------|-------------|-----|
| `shell=True` with untrusted input | Shell injection vulnerability | Pass a list of arguments; avoid `shell=True` with any user-supplied data |
| Not setting `text=True` | stdout/stderr come back as `bytes`, not `str` | Pass `text=True` (or decode manually) when you want strings |
| Ignoring `returncode` without `check=True` | Silent failures treated as success | Use `check=True` and catch `CalledProcessError`, or inspect `returncode` explicitly |
| Deadlock piping large output through `Popen` without draining it | Both processes block once the OS pipe buffer fills | Use `subprocess.run()`/`communicate()`, which drain both streams for you |
| Calling `os.fork()` on Windows | `AttributeError: module 'os' has no attribute 'fork'` | `os.fork` is POSIX-only; use `subprocess` or `multiprocessing` for portability |
