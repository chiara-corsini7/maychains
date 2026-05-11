#! python

import numpy as np
import gsd.hoomd
import argparse
import string

def read_bonds_from_topo_file(file):
    print('Getting Topology...')
    bonds = []
    with open(file) as f:
        while True:
            line = f.readline()
            if not line:
                break
            if line.strip() == "Bonds":
                print('... Bonds...')
                # Move to first bond line
                line = f.readline()
                while True:
                    if not line:
                        print("Warning: Reached EOF before 'Angles'")
                        break
                    if line.strip() == "Angles":
                        break
                    data = line.strip().split()
                    if len(data) == 4:
                        #print('bond')
                        bonds.append([int(data[-2]) - 1,
                                      int(data[-1]) - 1])
                    line = f.readline()
    return np.asarray(bonds)


parser = argparse.ArgumentParser(description='Make a gsd trajectory from a lmps trajectory')

non_opt = parser.add_argument_group('mandatory arguments')

non_opt.add_argument('-i','--input', metavar="<dump>", type=str,dest='input_file', required=True,
    help="lammps dump file to extract from")

non_opt.add_argument('-t','--topology', metavar="<dump>", type=str,dest='topology', required=True,
    help="lammps \"topology\" file to extract from")

non_opt.add_argument('-o','--out', metavar='<gsd>', dest='output_file', required=True,
                   help='Name for the output gsd trajectory')
non_opt.add_argument('-n',\
                dest='numTrj', type=int,\
                required=True, help='Number of dump files')

args = parser.parse_args()
input_file = args.input_file
topo_file = args.topology
output_file = args.output_file
numTrj = args.numTrj
# input_file = '/Users/weiimac/cluster_mount/dynamic-nw/nvt-penetrant/dp2.00-Np1/f_0.111-lambda1.2/T0.62-536345842/dump-3b-T0.62-eq-'
# topo_file = '/Users/weiimac/cluster_mount/dynamic-nw/nvt-penetrant/dp2.00-Np1/f_0.111-lambda1.2/T0.62-536345842/config-3b-T0.62'
# output_file = './dyn-nw-pene.gsd'

input_1 = input_file

print("Creating gsd trajectory from lmps trajectory:")
t =  gsd.hoomd.open(name=output_file, mode='w')
print("Inputs:",input_file,topo_file)
print("Output:",output_file)

bonds = read_bonds_from_topo_file(topo_file)

timestep = -1
print('Converting Trajectory...')
with open(input_1) as f:
    while True:
        line=f.readline()
        if line.strip() == "ITEM: TIMESTEP":
            nexline=f.readline()
            timestep += int(1) 
#int(nexline.strip())
            coords=[]
            box = []
            read = False
        if "ITEM: NUMBER OF ATOMS" in line:
            nexline=f.readline()
            num =int(nexline.strip())
        if "ITEM: BOX" in line:
            for i in range(3):
                nextline=f.readline()
                box.append(float(nextline.strip().split()[1])- float(nextline.strip().split()[0]))
        if "ITEM: ATOM" in line:
            for i in range(num):
                nextline=f.readline()
                coords.append(nextline.strip().split())
            read = True
        if read == True:
            box=np.array(box)
            coords=np.asarray(coords)
            # ITEM: ATOMS id mol type mass q x y z
            ids=coords.T[-8].astype(int) - np.ones(len(coords), dtype=int)
            #print(ids)
            sorted_coords = coords[np.argsort(ids)]

            type_ids=(sorted_coords.T[-6:-5].T).astype(int)-1
            charges=(sorted_coords.T[-4:-3].T).astype(int)
            positions=(sorted_coords.T[-3:].T).astype(float)
            mole_ids = (sorted_coords.T[-7:-6].T).astype(int)-1
            #print(mole_ids)
            # invent particle type names
            
            u = np.unique(type_ids)
            u = u - np.min(u)
            typeMax = len(u)
            u[-1] = typeMax
            u = np.arange(0, typeMax+1, 1, dtype=int)
            letter_list = [string.ascii_uppercase[a] for a in u]
            if timestep==0:
                print(letter_list)

            # make a new gsd frame
       ##     s1 = gsd.hoomd.Snapshot()
            s1 = gsd.hoomd.Frame()
            s1.configuration.step=timestep
            s1.configuration.box=np.array([box[0],box[1],box[2],0,0,0])
            s1.configuration.dimensions=3
            s1.particles.types=letter_list

            s1.bonds.N=len(bonds)
            s1.bonds.types=['bond']
            s1.bonds.typeid=np.zeros(len(bonds))
            s1.bonds.group =bonds

            s1.particles.N=len(positions)
            s1.particles.typeid=type_ids
            s1.particles.position=positions
            s1.particles.charge=charges
            s1.particles.body=mole_ids
            #s1.particles.velocity= np.zeros_like(positions)
            #s1.particles.image= np.zeros_like(positions)
            
            if not line.strip()=="": # to avoid printing out the last frame twice
                t.append(s1)
                timeend = timestep
        if not line: break
print(f"timeend = {timeend}")

if numTrj > 1 :
    for nTrj in range(1, numTrj):
        print(f"timeend*i = {timeend*nTrj}")
        # input_2 = input_file + {i+1} + ".bin.txt"
        input_2 = f"{input_file}{nTrj+1}.bin.txt"
        print(input_2)
        with open(input_2) as f:
            while True:
                line=f.readline()
                if line.strip() == "ITEM: TIMESTEP":
                    nexline=f.readline()
                    timestep = int(nexline.strip())
                    coords=[]
                    box = []
                    read = False
                if "ITEM: NUMBER OF ATOMS" in line:
                    nexline=f.readline()
                    num =int(nexline.strip())
                if "ITEM: BOX" in line:
                    for i in range(3):
                        nextline=f.readline()
                        box.append(float(nextline.strip().split()[1])- float(nextline.strip().split()[0]))
                if "ITEM: ATOM" in line:
                    for i in range(num):
                        nextline=f.readline()
                        coords.append(nextline.strip().split())
                    read = True
                if read == True:
                    box=np.array()
                    coords=np.asarray(coords)
                    # ITEM: ATOMS id mol type mass q x y z
                    type_ids=(coords.T[-6:-5].T).astype(int)-1
                    positions=(coords.T[-3:].T).astype(float)
                    # invent particle type names
                    u = np.unique(type_ids)
                    u = u - np.min(u)
                    typeMax = len(u)
                    u[-1] = typeMax
                    u = np.arange(0, typeMax+1, 1, dtype=int)
                    letter_list = [string.ascii_uppercase[a] for a in u]
    
                    # make a new gsd frame
                   # s1 = gsd.hoomd.Snapshot()
                    s1 = gsd.hoomd.Frame()
                    s1.configuration.step=timestep + timeend*nTrj # becasue each trj file starts from 0, need to make sure the timestep is increasing
                    s1.configuration.box=np.array([box[0],box[1],box[2],0,0,0])
                    s1.configuration.dimensions=3
                    s1.particles.types=letter_list
    
                    s1.bonds.N=len(bonds)
                    s1.bonds.types=['bond']
                    s1.bonds.typeid=np.zeros(len(bonds))
                    s1.bonds.group =bonds
    
                    s1.particles.N=len(positions)
                    s1.particles.typeid=type_ids
                    s1.particles.position=positions
                    s1.particles.charge=charges
                    s1.particles.body=mole_ids
                    #s1.particles.velocity= np.zeros_like(positions)
                    #s1.particles.image= np.zeros_like(positions)
                    
                    # print(timestep)
                    if not line.strip()=="":
                        if timestep != 0: # to skip the first frame in the second trj file because it's the same as the last frame in the first trj file
                            t.append(s1)
                if not line: break
    
        print(f"{timeend*nTrj}")


print("DONE")
