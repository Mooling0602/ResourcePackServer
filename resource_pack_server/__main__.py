def main():
    """Entry point for `python -m resource_pack_server` or the console script."""
    try:
        from mcdreforged.api.all import ServerInterface

        psi = ServerInterface.psi_opt()
        if psi is not None:
            # Running inside MCDR — delegate to MCDR entrypoint
            from resource_pack_server.mcdr.mcdr_entrypoint import on_load
            on_load(psi, None)
            return
    except Exception:
        pass

    # Standalone mode
    from resource_pack_server.cli.cli_entrypoint import cli_entry

    cli_entry()


if __name__ == "__main__":
    main()
