import sys

from rich import print
import typer

from ...context import ctx

app = typer.Typer(
    help="Mail diagnostics.",
    no_args_is_help=True,
)


@app.callback()
def mail():
    pass


@app.command("test", help="Send a test email to verify the SMTP configuration.")
def app_test(
    to: str = typer.Argument(
        ...,
        help="Recipient email address.",
    ),
    subject: str = typer.Option(
        "lncrawl SMTP test",
        "--subject",
        "-s",
        help="Subject line for the test message.",
    ),
):
    cfg = ctx.config.mail
    print("[bold]SMTP configuration[/bold]")
    print(f"  server:   [cyan]{cfg.smtp_server}:{cfg.smtp_port}[/cyan]")
    print(f"  username: [cyan]{cfg.smtp_username or '(empty)'}[/cyan]")
    print(f"  sender:   [cyan]{cfg.smtp_sender or cfg.smtp_username or '(empty)'}[/cyan]")
    print(f"  password: [cyan]{'set' if cfg.smtp_password else '(empty)'}[/cyan]")

    body = (
        "<html><body>"
        "<h2>lncrawl SMTP test</h2>"
        "<p>If you can read this, SMTP delivery from lncrawl is working.</p>"
        "</body></html>"
    )

    try:
        ctx.mail.send(to, subject, body)
    except Exception as e:
        print(f"[red]Send failed:[/red] {e!r}")
        cause = e.__cause__
        if cause is not None:
            print(f"[red]Underlying error:[/red] {cause!r}")
        sys.exit(1)
    finally:
        ctx.mail.close()

    print(f"[green]Sent test email to {to}.[/green]")
