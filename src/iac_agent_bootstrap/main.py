from iac_agent_bootstrap.bootstrap_workflow import BootstrapWorkflow


def main() -> None:
    result = BootstrapWorkflow().run(
        repos_path="data/repositories",
    )

    print("Bootstrap completed")
    print(result)


if __name__ == "__main__":
    main()