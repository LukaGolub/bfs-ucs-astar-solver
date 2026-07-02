import sys
import heapq
import argparse
from collections import deque

def bfs(start, ciljevi, graf):
    open_list = deque([(start, [start], 0.0)])
    visited = set()
    u_redu = {start}                                #Ovo prati tko je posjecen pa ubrza bfs, bez njega 3x3 slagalice timeouta
    brojac = 0
    while open_list:
        trenutno, put, trosak = open_list.popleft() #FIFO tj uzima onog koji je zadnji usao
        if trenutno in visited: continue
        visited.add(trenutno)
        brojac += 1
        if trenutno in ciljevi:
            return True, brojac, len(put), trosak, put
        if trenutno in graf:
            for susjed, cijena in graf[trenutno]:
                if susjed not in visited and susjed not in u_redu:
                    u_redu.add(susjed)
                    open_list.append((susjed, put + [susjed], trosak + cijena))
    return False, brojac, 0, 0, []

def ucs(start, ciljevi, graf):
    open_list = [(0.0, start, [start])]         #Sorta po velicini troska
    visited = set()
    brojac = 0
    while open_list:
        trosak, trenutno, put = heapq.heappop(open_list)    #Uzima onog s najmanjim troskom
        if trenutno in visited: continue
        visited.add(trenutno)
        brojac += 1
        if trenutno in ciljevi:
            return True, brojac, len(put), trosak, put
        if trenutno in graf:
            for susjed, cijena in graf[trenutno]:
                if susjed not in visited:
                    heapq.heappush(open_list, (trosak + cijena, susjed, put + [susjed]))
    return False, brojac, 0, 0, []

def astar(start, ciljevi, graf, h):
    open_list = [(h[start], 0.0, start, [start])]
    closed = {} 
    brojac = 0
    while open_list:
        f, g, trenutno, put = heapq.heappop(open_list)          #Vadi onaj s najmanjim f
        if trenutno in closed and closed[trenutno] <= g: continue
        closed[trenutno] = g        #Ako je trenutni put bolji, zapisi ga
        brojac += 1
        if trenutno in ciljevi:
            return True, brojac, len(put), g, put
        if trenutno in graf:
            for susjed, cijena in graf[trenutno]:
                novi_g = g + cijena
                if susjed not in closed or novi_g < closed[susjed]:
                    novi_f = novi_g + h.get(susjed, 0.0)        #Uzmi procjenu iz heuristike
                    heapq.heappush(open_list, (novi_f, novi_g, susjed, put + [susjed]))
    return False, brojac, 0, 0, []

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--alg') 
    p.add_argument('--ss') 
    p.add_argument('--h')
    p.add_argument('--check-optimistic', action='store_true')
    p.add_argument('--check-consistent', action='store_true')
    args = p.parse_args()

   
    f = open(args.ss, 'r', encoding='utf-8') #Datoteka prostora stanja
    linije = []
    for l in f:
        l = l.strip()
        if l and not l.startswith('#'):
            linije.append(l)
    f.close()
    
    start = linije[0]
    ciljevi = set(linije[1].split())
    graf = {}                           #Stvaranje grafa
    for i in range(2, len(linije)):
        stanje, susjedi_tekst = linije[i].split(':')
        stanje = stanje.strip()
        popis_susjeda = []
        if susjedi_tekst.strip():
            for s in susjedi_tekst.strip().split():
                ime, cijena = s.split(',')
                popis_susjeda.append((ime, float(cijena)))
        popis_susjeda.sort()
        graf[stanje] = popis_susjeda

   
    h = {}
    if args.h:          #Datoteka heuristike
        f_h = open(args.h, 'r', encoding='utf-8')
        for l in f_h:
            l = l.strip()
            if ':' in l and not l.startswith('#'):
                s, v = l.split(':')
                h[s.strip()] = float(v.strip())
        f_h.close()

    
    if args.check_optimistic:       #Provjera optimističnosti
        print(f"# HEURISTIC-OPTIMISTIC {args.h}")
        svi_ok = True
        for s in sorted(h.keys()):
            found, _, _, h_star, _ = ucs(s, ciljevi, graf)
            ok = h[s] <= h_star
            if not ok: svi_ok = False
            print(f"[CONDITION]: [{'OK' if ok else 'ERR'}] h({s}) <= h*: {h[s]:.1f} <= {h_star:.1f}")
        print(f"[CONCLUSION]: Heuristic is {'optimistic.' if svi_ok else 'not optimistic.'}")

    elif args.check_consistent:         #Provjera konzistenstnosti
        print(f"# HEURISTIC-CONSISTENT {args.h}")
        svi_ok = True
        for s in sorted(h.keys()):
            if s in graf:
                for susjed, cijena in graf[s]:
                    if susjed in h:
                        ok = h[s] <= h[susjed] + cijena
                        if not ok: svi_ok = False
                        print(f"[CONDITION]: [{'OK' if ok else 'ERR'}] h({s}) <= h({susjed}) + c: {h[s]:.1f} <= {h[susjed]:.1f} + {cijena:.1f}")
        print(f"[CONCLUSION]: Heuristic is {'consistent.' if svi_ok else 'not consistent.'}")

    else:
        if args.alg == 'bfs':
            print("# BFS")
            rez = bfs(start, ciljevi, graf)
        elif args.alg == 'ucs':
            print("# UCS")
            rez = ucs(start, ciljevi, graf)
        elif args.alg == 'astar':
            print(f"# A-STAR {args.h}")
            rez = astar(start, ciljevi, graf, h)
        
        ok, posj, dulj, cijena, put = rez
        print(f"[FOUND_SOLUTION]: {'yes' if ok else 'no'}")
        if ok:
            print(f"[STATES_VISITED]: {posj}")
            print(f"[PATH_LENGTH]: {dulj}")
            print(f"[TOTAL_COST]: {cijena:.1f}")
            print(f"[PATH]: {' => '.join(put)}")


main()
