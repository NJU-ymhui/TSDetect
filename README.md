# TSDetect
A tool for detecting python test smell 

## How To Run
### Windows

1. Add your to-be-tested **Python** `file` or `projects` into TSDetect/tests/resources
2. Find TSDetect/start.bat
3. Click start.bat

## Get Better Result
If you can provide the initial java codes which are the tested codes of the unit tests in `src/resources`, you can get better result.
<br>
1. Rename your unit test file to `{$TESTED_CLASS_NAME}_test.py`, this may not satisfy the naming rule, but it can help the tool to find the tested class.
2. Ensure your source tested codes are named with `{$TESTED_CLASS_NAME}.py`. For example, if you have a class named `Foo`, 
you should name the tested code as `Foo.py`, and relatively the unit test file should be named as `Foo_test.py`.
3. Ensure the relative path of the source tested codes and the unit test file are the same. For example, if the unit test file 
path is `tests/resources/path/to/your/unit_test/Foo_test.py`, the source tested codes put in `src/resources` 
should be `src/resources/path/to/your/unit_test/Foo.py`, and now this tool can find the source tested codes 
of the unit test.
4. Follow the above protocols and this tool can bind your unit test with the source tested codes, 
so you can get better result!