# Wakatime Updater Stats README

This application updates images that can be used in your GitHub profile READMEs. It is specifically designed to create SVG images based on your WakaTime statistics.

## How It Works

1. Define the environment variables:
    - [WAKATIME_API_KEY](https://wakatime.com/api-key) found in the settings of your Wakatime account
    - GITHUB_USER your username on GitHub
    - [GITHUB_TOKEN](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) you need to create this token. I recommend using the following options:
        - public_repo
        - read:project
        - read:user

2. Deploy with [GitHub Actions](https://docs.github.com/en/actions)

## Inspiration

This application was inspired by the original work of Avinal Kumar. You can find the original author's repository at the following address: https://github.com/avinal/Profile-Readme-WakaTime

## License

MIT License

Copyright (c) 2021 Avinal Kumar

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
