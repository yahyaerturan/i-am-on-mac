# i-am-on-mac

## Coreutils

Make sure you install `coreutils` first:

```bash
brew install coreutils
```

## zsh

Open your `~/.zshrc` file and add this line:

`source $HOME/Code/misc/i-am-on-mac/.my_zsh`

## Sublime Text

```bash
sudo ln -s /Applications/Sublime\ Text.app/Contents/SharedSupport/bin/subl /usr/local/bin/sublime
```

## Docker SSH


```
chmod a+x bin/docker-ssh
```

## Understanding exit codes

- 1 - Catchall for general errors
- 2 - Misuse of shell builtins (according to Bash documentation)
- 126 - Command invoked cannot execute
- 127 - “command not found”
- 128 - Invalid argument to exit
- 128+n - Fatal error signal “n”
- 130 - Script terminated by Control-C
- 255\* - Exit status out of range
