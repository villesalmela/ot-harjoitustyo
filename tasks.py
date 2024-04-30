from invoke.tasks import task

@task
def start(ctx):
    ctx.run("python3 src/main.py")

@task
def test(ctx):
    ctx.run("pytest src/tests")

@task
def coverage(ctx):
    ctx.run("coverage run")

@task(coverage)
def coverage_report(ctx):
    ctx.run("coverage html")

@task
def lint(ctx):
    ctx.run("pylint src")

@task
def format(ctx):
    ctx.run("autopep8 src")