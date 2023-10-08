from glob import glob
from os import path, unlink
from os.path import basename, splitext
from pathlib import Path
from subprocess import run
from redmail import EmailSender
from atexit import register


# noinspection PyShadowingNames
def split(
    src: str,
    tar_dir: str = 'output',
    tar_name: str = None,
    split_size: int = 20
) -> list[str]:
    tar_dir = tar_dir or '.'
    Path(tar_dir).mkdir(parents=True, exist_ok=True)
    tar_name = tar_name or splitext(basename(src))[0] + '.zip'
    tar_path = path.join(tar_dir, tar_name)
    tar_pattern = splitext(tar_path)[0] + '.z*'
    files = glob(tar_pattern)
    if not files:
        run(['zip', '-s', f'{split_size}m', tar_path, src])
        files = glob(tar_pattern)
    return sorted(files)


smtp = EmailSender(
    host='smtp.qq.com',
    port=587,
    username='abc@qq.com',
    password='owhuzq'
)
smtp.receivers = 'qwe@qq.com'

src = 'C:\\a.exe'

if __name__ == '__main__':
    output = split(src)
    for o in output:
        print(f'Sending {o} ...', end=' ')
        smtp.send(
            subject=' ',
            attachments={basename(o): Path(o)}
        )
        print('Done')


    @register
    def clean():
        # noinspection PyShadowingNames
        for o in output: unlink(o)
