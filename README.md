# TSDetect
A tool for detecting Go test smell 

## How To Run
### Windows

1. Add your to-be-tested **Go** `file` or `projects` into TSDetect/tests/resources
2. Find TSDetect/start.bat
3. Click start.bat

## Get Better Result
If you can provide the initial go codes which are the tested codes of the unit tests in `src/resources`, you can get better result.
<br>
1. Rename your unit test file to `{$SRC_TESTED_FILE_NAME}_test.go`, this may not satisfy the naming rule, but it can help the tool to find the 
source tested file.
2. Ensure your source tested codes are named with `{$SRC_TESTED_FILE_NAME}.go`. For example, if you have a source tested 
file named `foo.go`, and relatively the unit test file should be named as `foo_test.go`.
3. Ensure the relative path of the source tested codes and the unit test file are the same. For example, if the unit test file 
path is `tests/resources/path/to/your/unit_test/foo_test.go`, the source tested codes put in `src/resources` 
should be `src/resources/path/to/your/unit_test/foo.go`, and now this tool can find the source tested codes 
of the unit test.
4. Follow the above protocols and this tool can bind your unit test with the source tested codes, 
so you can get better result!