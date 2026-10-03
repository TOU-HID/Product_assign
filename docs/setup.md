# React Native CLI + TypeScript + Yarn setup on your Mac

**Goal:** run a basic app on Android and iOS before adding assignment features.

**File placement:** all Markdown files stay in `product_assignment/docs`. Application code stays in `ShopDiscover/`.

You will type the commands yourself. Follow one step at a time. If a command fails, stop there and share its error before continuing.

Your Mac already has Node, npm, Java 17, Watchman, Ruby, Bundler, CocoaPods, Xcode, and Android SDKs installed. The steps below verify and use them; you do not need to reinstall everything.

## 1. Check the installed tools

Open Terminal and run:

```bash
node --version
npm --version
watchman --version
java -version
ruby --version
bundle --version
pod --version
xcodebuild -version
adb --version
```

**Check:** each command prints a version instead of “command not found.” Java should be version 17. The current React Native environment guide requires Node 22.11.0 or newer; your checked version is Node 24.

### Check Yarn

```bash
yarn --version
```

If it prints a version, Yarn is available. Continue to Step 2.

If Yarn is missing, check Corepack, which manages Yarn versions:

```bash
corepack --version
```

Only if Corepack is also missing, install it:

```bash
npm install -g corepack
```

Then enable Yarn:

```bash
corepack enable
corepack install --global yarn@stable
yarn --version
```

**Check:** Yarn prints a version. We will use Yarn to install app packages and run app commands. npm/npx are used only for initial tooling and the React Native generator.

| Tool | Simple explanation |
| --- | --- |
| Node | Run JavaScript development tools. |
| Yarn | Install app packages and run the project's commands. |
| npm/npx | Bootstrap tools and run the React Native generator. |
| Watchman | Watch your files for changes. |
| Java + Android SDK | Build the Android app. |
| ADB | Connect your computer to an Android device/emulator. |
| Xcode | Build the iOS app and provide simulators. |
| Ruby + Bundler | Run and manage Ruby tools used for iOS dependencies. |
| CocoaPods | Install native iOS libraries. |

## 2. Tell your terminal where Java and Android tools live

Open your terminal configuration:

```bash
nano ~/.zshrc
```

Look for existing Java/Android settings. Add or correct the following lines; avoid duplicate or conflicting settings:

```bash
export JAVA_HOME=$(/usr/libexec/java_home -v 17)
export ANDROID_HOME="$HOME/Library/Android/sdk"
export PATH="$PATH:$ANDROID_HOME/emulator:$ANDROID_HOME/platform-tools"
```

What they mean:

- `JAVA_HOME`: location of Java 17.
- `ANDROID_HOME`: location of the Android SDK. This is your Mac's checked SDK path.
- `PATH`: lets you run Android commands without typing their full locations.

Save in nano: **Control + O → Enter → Control + X**.

Load your changes:

```bash
source ~/.zshrc
echo "$JAVA_HOME"
echo "$ANDROID_HOME"
adb --version
```

**Check:** the first two commands print folder paths; the last prints the ADB version.

## 3. Start an Android emulator

This step uses Android Studio's interface.

1. Open **Android Studio → Device Manager**. On the welcome screen, look under **More Actions**.
2. Start an existing phone emulator, or choose **Create Device**.
3. If creating one, choose a phone such as a Pixel and an **ARM64** system image for your Apple Silicon Mac.
4. Finish creation and click the play button.
5. Wait until the Android home screen appears.

In **SDK Manager**, check that SDK Platform, Build-Tools, Platform-Tools, Emulator, and Command-line Tools are installed. Your Mac already has SDK platforms 35/36 and Build-Tools 36.0.0. If the generated project requires another version, install that version through SDK Manager; do not change project versions just to suppress a missing-SDK error.

Run:

```bash
adb devices
```

**Check:** a device such as `emulator-5554` appears with status `device`.

## 4. Prepare the iOS simulator

1. Open **Xcode** and finish any first-launch installation.
2. In **Xcode → Settings → Locations**, select Xcode under **Command Line Tools**.
3. In **Settings → Components/Platforms**, install an iOS simulator runtime if missing. The label depends on the Xcode version.

Run:

```bash
xcode-select -p
xcrun simctl list devices available
```

**Check:** the developer path points to your Xcode installation and available iPhone simulators are listed.

Only if the developer path is incorrect, run:

```bash
sudo xcode-select --switch /Applications/Xcode.app/Contents/Developer
```

`sudo` requests your Mac password. Password characters do not appear while typing.

Simulator availability must be checked in your own terminal; the assistant's restricted environment could not verify simulator services.

## 5. Create the app

We will use **ShopDiscover** as the app name. You may choose another name before creation; then replace it consistently in later commands.

If you previously installed a global React Native CLI, remove it first:

```bash
npm uninstall -g react-native-cli @react-native-community/cli
```

Now create the project:

```bash
cd /Users/md.touhidulislam/Projects/product_assignment
npx @react-native-community/cli@latest init ShopDiscover --pm yarn
```

- `cd`: move into a folder.
- `npx`: run the CLI without installing it globally.
- `init ShopDiscover`: create the basic native app.
- `--pm yarn`: use Yarn to install and manage the app's packages.

Using `npx` to launch the generator does not make the app an npm project; `--pm yarn` selects its package manager.

Accept the package-install prompt. If asked to install CocoaPods, choose **yes**.

**TypeScript is included by default. Do not add a separate TypeScript template.**

Move into the new app folder:

```bash
cd ShopDiscover
```

Check the project's Yarn version and dependency layout:

```bash
yarn --version
```

The generator may select a project-specific Yarn version. Keep its generated settings. For Yarn 2 or newer, check:

```bash
yarn config get nodeLinker
```

**Check:** it prints `node-modules`. If it prints something else, run:

```bash
yarn config set nodeLinker node-modules
yarn install
```

This makes Yarn install packages in the `node_modules` folder used by React Native tooling. Yarn 1 already uses that layout; skip the `nodeLinker` commands for Yarn 1.

Your folders will look like this:

```text
product_assignment/
  docs/
    plan.md
    next-steps.md
    setup.md
    README.md
  ShopDiscover/
    android/
    ios/
    App.tsx
    package.json
    yarn.lock
    tsconfig.json
```

**Check:** `ShopDiscover` contains `App.tsx`, `android`, and `ios`. Run future app commands inside this folder.

## 6. Finish iOS dependency installation if needed

If the creation step successfully installed CocoaPods, skip this step.

Otherwise, from `ShopDiscover`, run:

```bash
bundle install
cd ios
bundle exec pod install
cd ..
```

- `bundle install`: install the Ruby tools specified by the project's Gemfile.
- `bundle exec pod install`: install native iOS libraries using those tool versions.
- `cd ..`: return to the app folder.

**Check:** CocoaPods finishes successfully. You are back inside `ShopDiscover`.

## 7. Start Metro — terminal 1

Run:

```bash
cd /Users/md.touhidulislam/Projects/product_assignment/ShopDiscover
yarn start
```

**Leave this terminal running.**

Metro prepares and serves your JavaScript/TypeScript code to the app during development. It does not build the native Android/iOS app itself.

**Check:** Metro starts and waits for app connections.

## 8. Run Android — terminal 2

Keep the Android emulator open. Open another terminal tab/window and run:

```bash
cd /Users/md.touhidulislam/Projects/product_assignment/ShopDiscover
yarn android
```

This builds, installs, and launches the Android app. The first build can take several minutes because it downloads build dependencies.

**Check:** the starter app appears in your Android emulator.

## 9. Run iOS — terminal 3

Open another terminal tab/window and run:

```bash
cd /Users/md.touhidulislam/Projects/product_assignment/ShopDiscover
yarn ios
```

This builds and launches the app in an iOS simulator.

If you need to select a particular simulator, list devices:

```bash
xcrun simctl list devices available
```

Then use a name from that list:

```bash
yarn ios --simulator="EXACT SIMULATOR NAME"
```

Replace `EXACT SIMULATOR NAME` before running that command.

**Check:** the starter app appears in an iPhone simulator.

## 10. Make your first change and check TypeScript

Open the app folder in your editor. Change some visible text in `App.tsx`, save, and confirm both apps show the change.

| File/folder | What it does |
| --- | --- |
| `App.tsx` | Main React component; `.tsx` means TypeScript with JSX. |
| `tsconfig.json` | Type-checking settings. |
| `index.js` | Registers the app. Keep its generated extension. |
| `package.json` | Lists packages and commands such as `start` and `android`. |
| `android/` | Native Android project. |
| `ios/` | Native iOS project. |

From the app folder, run:

```bash
yarn tsc --noEmit
yarn lint
```

- TypeScript checks that values and functions use compatible types.
- `--noEmit` checks without generating JavaScript files.
- Lint checks the code against the project's configured rules.

Babel transforms TypeScript during bundling. Running the app does not replace a separate type check.

**Check:** both commands finish successfully, and your text change appears on both platforms.

## 11. Save your working setup in Git

Inside `ShopDiscover`, run:

```bash
git status
```

If it says this is not a Git repository, initialize one:

```bash
git init
```

Then run:

```bash
git add .
git diff --cached --stat
git commit -m "chore: verify React Native TypeScript setup on Android and iOS"
```

Use that message after both platforms actually work. If there are no changes to commit, the CLI may already have committed the starter; inspect it with `git log --oneline` and commit your own text change when ready.

Keep `yarn.lock`, the project's Yarn version setting in `package.json`, any generated `.yarnrc.yml`, and native dependency lockfiles in Git. They help another person install the same dependency versions. Use Yarn consistently for app packages; avoid creating a second JavaScript lockfile with `npm install`.

This repository is inside `ShopDiscover`; all Markdown files, including the moved starter README, now stay in the parent folder's `docs` directory. Include these documents when preparing the assignment submission.

## Daily commands to remember

From `ShopDiscover`:

| Purpose | Command |
| --- | --- |
| Install packages already listed in `package.json` | `yarn install` |
| Add an app dependency | `yarn add PACKAGE_NAME` |
| Add a development dependency | `yarn add -D PACKAGE_NAME` |
| Start Metro in its own terminal | `yarn start` |
| Build/run Android | `yarn android` |
| Build/run iOS | `yarn ios` |
| Check types | `yarn tsc --noEmit` |
| Check lint rules | `yarn lint` |
| Inspect your changes | `git status` |

Stop Metro with **Control + C** when you finish.

Replace `PACKAGE_NAME` with the actual package name when adding a dependency. CocoaPods still uses `bundle exec pod install`; Yarn manages JavaScript packages, while CocoaPods manages native iOS libraries.

## Setup is complete when

- [ ] Android app runs.
- [ ] iOS app runs.
- [ ] Your own text change appears on both.
- [ ] TypeScript and lint checks pass.
- [ ] Your actual work is saved in Git.

Then we can begin fetching and displaying products.

## Official references

- [Environment setup](https://reactnative.dev/docs/set-up-your-environment)
- [React Native CLI project creation](https://reactnative.dev/docs/getting-started-without-a-framework)
- [TypeScript support](https://reactnative.dev/docs/typescript)
- [Yarn installation](https://yarnpkg.com/getting-started/install)
- [Yarn dependency layout (`nodeLinker`)](https://yarnpkg.com/configuration/yarnrc#nodeLinker)

These instructions were checked against the official guides during this conversation. The initialization command chooses the current default release; record the generated React Native version from `package.json` for your README.
