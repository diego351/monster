import subprocess

class MemInfo:
    def report(self):
        top_ps = subprocess.Popen(['top', '-l', '1'], stdout=subprocess.PIPE)
        phys_mem = subprocess.check_output(('grep', 'PhysMem'), stdin=top_ps.stdout)
        top_ps.wait()

        phys_mem = phys_mem.strip().split() 
        free = int(phys_mem[9][:-1])
        used = int(phys_mem[7][:-1])
        active = int(phys_mem[3][:-1])
        inactive = int(phys_mem[5][:-1])
        wired = int(phys_mem[1][:-1])
        total = free + used

        return { 
                "free": free,
                "used": used,
                "active": active,
                "inactive": inactive,
                "wired": wired,
                "total": total,
        }
