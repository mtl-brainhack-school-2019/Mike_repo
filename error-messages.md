# A memory problem with VS Code...
    # Error message: "Visual Studio Code is unable to watch for file changes in this large workspace" (error ENOSPC)
    # What is this about?

    When you see this notification, it indicates that the VS Code file watcher is running out of handles because the workspace is large and contains many files. The current limit can be viewed by running:

    cat /proc/sys/fs/inotify/max_user_watches

    The limit can be increased to its maximum by editing /etc/sysctl.conf and adding this line to the end of the file:

    fs.inotify.max_user_watches=524288

    more at https://code.visualstudio.com/docs/setup/linux#_visual-studio-code-is-unable-to-watch-for-file-changes-in-this-large-workspace-error-enospc



# Computer dead... not much hope
    But see https://ubuntuforums.org/showthread.php?t=858104

    