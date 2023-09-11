from ali_ddns import DDdns
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledText
from ttkbootstrap import StringVar
import json
import threading
import ctypes
import logging
from logger import log, QueueFileHandler
from queue import Queue


class MyUI:
    def __init__(self, master):
        self.master = master
        self.root = ttk.Frame(master, padding=10)
        self.root.pack(fill=BOTH, expand=YES)
        self.style = ttk.Style()
        self.style.theme_use('united')
        self.ddns_thread = None

    def theme_generator(self):
        theme_bar = ttk.Frame(self.root, padding=10)
        theme_bar.pack(fill=X, expand=YES, anchor=N)
        theme_bar.grid_columnconfigure(0, weight=1)

        title = ttk.Label(
            master=theme_bar, text="阿里云DDNS", font="-size 40 -weight bold"
        )
        title.grid(column=0, row=0, rowspan=2, sticky=W)

        theme = StringVar()
        theme_lbl = ttk.Label(theme_bar, text="切换主题")
        theme_lbl.grid(column=1, row=0)
        theme_btn = ttk.Checkbutton(
            master=theme_bar, style=SQUARE + TOGGLE, variable=theme,
            offvalue='united', onvalue='darkly',
            command=lambda: self.style.theme_use(theme.get())
        )
        theme_btn.grid(column=2, row=0, sticky=E)

        transparent_lbl = ttk.Label(theme_bar, text="透  明  度")
        transparent_lbl.grid(column=1, row=1)
        transparent_scale = ttk.Scale(
            master=theme_bar, orient=HORIZONTAL, value=1, from_=1, to=0.4, length=0,
            command=lambda transparent: self.master.attributes("-alpha", transparent)
        )
        transparent_scale.grid(column=2, row=1, sticky=E)

    def conf_generator(self):
        cfg_bar = ttk.Frame(self.root, padding=10)
        cfg_bar.pack(fill=X, expand=YES, anchor=N)

        accessKeyId_lbl = ttk.Label(master=cfg_bar, text='accessKeyId')
        accessKeyId_lbl.grid(column=0, row=0, sticky=W)
        self.accessKeyId_entry = ttk.Entry(cfg_bar, width=30)
        self.accessKeyId_entry.grid(column=1, row=0, padx=20, pady=5)

        accessKeySecret_lbl = ttk.Label(master=cfg_bar, text='accessKeySecret')
        accessKeySecret_lbl.grid(column=0, row=1, sticky=W)
        self.accessKeySecret_entry = ttk.Entry(cfg_bar, width=30)
        self.accessKeySecret_entry.grid(column=1, row=1, padx=20, pady=5)

        domain_name_lbl = ttk.Label(master=cfg_bar, text='domain_name')
        domain_name_lbl.grid(column=0, row=2, sticky=W)
        self.domain_name_entry = ttk.Entry(cfg_bar, width=30)
        self.domain_name_entry.grid(column=1, row=2, padx=20, pady=5)

        execute_btn = ttk.Button(master=cfg_bar, text='应用并启动', command=self.execute)
        execute_btn.grid(column=2, row=2)

        interval_lbl = ttk.Label(master=cfg_bar, text='interval')
        interval_lbl.grid(column=0, row=3, sticky=W)
        self.interval_cbo = ttk.Combobox(
            master=cfg_bar, width=5, values=('5', '10', '20', '30', '60'), state=READONLY
        )
        self.interval_cbo.current(1)
        self.interval_cbo.grid(column=1, row=3, sticky=W, padx=20, pady=5)
        interval_txt = ttk.Label(master=cfg_bar, text='minutes')
        interval_txt.grid(column=1, row=3, padx=10, pady=5)

    def set_cfg(self):
        log.info('读取本地配置')
        try:
            with open('cfg.json', 'r') as f:
                cfg = json.load(f)
            log.info('读取本地配置成功')
        except FileNotFoundError:
            log.info('无本地配置，应用后自动创建')
            return
        self.accessKeyId_entry.delete(0, END)
        self.accessKeyId_entry.insert(0, cfg['accessKeyId'])
        self.accessKeySecret_entry.delete(0, END)
        self.accessKeySecret_entry.insert(0, cfg['accessKeySecret'])
        self.domain_name_entry.delete(0, END)
        self.domain_name_entry.insert(0, cfg['domain_name'])
        self.interval_cbo.set(cfg['interval'])

    def read_cfg(self):
        cfg = {
            "accessKeyId": self.accessKeyId_entry.get(),
            "accessKeySecret": self.accessKeySecret_entry.get(),
            "domain_name": self.domain_name_entry.get(),
            "interval": int(self.interval_cbo.get())
        }
        return cfg

    def execute(self):
        cfg = self.read_cfg()
        with open('cfg.json', 'w') as f:
            json.dump(cfg, f, indent=2)
        log.info('应用配置成功')
        log.info('开始运行')
        if self.ddns_thread:  # 如果有ddns监听线程，则强制中断
            ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(self.ddns_thread.ident), ctypes.py_object(SystemExit))
            self.ddns_thread = None
        ddns = DDdns()
        self.ddns_thread = threading.Thread(target=ddns.run, args=(cfg,), daemon=True)
        self.ddns_thread.start()

    def log_generator(self):
        self.log_window = ScrolledText(master=self.root, height=10, width=60, autohide=True, padding=10)
        self.log_window.pack(fill=BOTH, expand=YES)

    def msg_setter(self):
        while True:
            msg = mq.get()
            self.log_window.insert(END, msg + '\n')

    def run(self):
        self.theme_generator()
        self.conf_generator()
        self.set_cfg()
        self.log_generator()
        msg_thread = threading.Thread(target=self.msg_setter, daemon=True)
        msg_thread.start()


if __name__ == '__main__':
    # 初始化日志
    mq = Queue()
    formatter = logging.Formatter('[%(asctime)s] [%(levelname)5s] %(message)s')
    qfh = QueueFileHandler(mq, filename='./ddns.log', encoding='utf8')
    qfh.setFormatter(formatter)
    log.addHandler(qfh)

    app = ttk.Window("ali_ddns_v1.0.0")
    ui = MyUI(app)
    ui.run()
    app.mainloop()
