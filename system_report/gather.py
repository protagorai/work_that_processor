import json
import platform
import subprocess
import shutil
from datetime import datetime
from pathlib import Path

try:
    import psutil
except ImportError:  # pragma: no cover - fallback when psutil is missing
    psutil = None

try:
    import cpuinfo  # type: ignore
except ImportError:  # pragma: no cover - fallback
    cpuinfo = None

try:
    import GPUtil  # type: ignore
except ImportError:  # pragma: no cover
    GPUtil = None

def _run_cmd(cmd):
    try:
        result = subprocess.check_output(cmd, shell=True, text=True)
        return result.strip()
    except Exception:
        return ""

def get_cpu_info():
    info = {
        "architecture": platform.machine(),
        "count": psutil.cpu_count(logical=False) if psutil else None,
        "count_logical": psutil.cpu_count() if psutil else None,
    }
    if cpuinfo:
        data = cpuinfo.get_cpu_info()
        info.update({
            "brand": data.get("brand_raw"),
            "hz_advertised": data.get("hz_advertised_friendly"),
            "l2_cache_size": data.get("l2_cache_size"),
            "l3_cache_size": data.get("l3_cache_size"),
            "arch": data.get("arch_string_raw"),
            "flags": data.get("flags"),
        })
    return info

def get_gpu_info():
    gpus = []
    if GPUtil:
        for gpu in GPUtil.getGPUs():
            gpus.append({
                "name": gpu.name,
                "total_memory": gpu.memoryTotal,
                "uuid": gpu.uuid,
                "driver": gpu.driver,
            })
    return gpus

def get_ram_info():
    if not psutil:
        return {}
    mem = psutil.virtual_memory()
    return {
        "total": mem.total,
        "available": mem.available,
    }

def get_storage_info():
    if not psutil:
        return []
    disks = []
    for part in psutil.disk_partitions():
        usage = psutil.disk_usage(part.mountpoint)
        disks.append({
            "device": part.device,
            "mountpoint": part.mountpoint,
            "fstype": part.fstype,
            "total": usage.total,
            "free": usage.free,
        })
    return disks

def get_installed_software():
    softwares = []
    if platform.system() == "Windows":
        cmd = "wmic product get name,version"
        out = _run_cmd(cmd)
        for line in out.splitlines()[1:]:
            if line.strip():
                softwares.append(line.strip())
    elif shutil.which("dpkg"):
        out = _run_cmd("dpkg -l | awk '{print $2" " $3}'")
        softwares = out.splitlines()
    elif shutil.which("rpm"):
        out = _run_cmd("rpm -qa")
        softwares = out.splitlines()
    return softwares

def docker_or_podman_installed():
    return shutil.which("docker") is not None or shutil.which("podman") is not None

def gather_all():
    data = {
        "timestamp": datetime.utcnow().isoformat(),
        "platform": platform.platform(),
        "cpu": get_cpu_info(),
        "gpu": get_gpu_info(),
        "ram": get_ram_info(),
        "storage": get_storage_info(),
        "installed_software": get_installed_software(),
        "docker_or_podman": docker_or_podman_installed(),
    }
    return data
