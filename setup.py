from cx_Freeze import setup, Executable

setup(name="Firecraze", version="1.0", executables=[Executable("game.py", icon="redplain.ico")], options={
    'build_exe': {
        'include_files': ['src/fonts', 'src/images', 'src/soundeffects']
    }
})
