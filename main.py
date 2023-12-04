from glob import glob
from os import path
from os.path import basename, splitext
from pathlib import Path
from subprocess import run

from redmail import EmailSender


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
        run(['zip', '-j', '-s', f'{split_size}m', tar_path, src])
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

def send(output: list[str], begin: int = None, end: int = None, ids_: list[int] = None) -> None:
    begin = begin or 1
    end = end or len(output)
    ids_ = ids_ or range(1, len(output) + 1)
    for i in range(begin, end + 1):
        if i not in ids_:
            continue

        print(f'Sending {output[i - 1]} ...', end=' ')
        smtp.send(
            subject=' ',
            attachments={basename(output[i - 1]): Path(output[i - 1])}
        )
        print('Done')


if __name__ == '__main__':
    output_ = split(src)
    send(output_)
