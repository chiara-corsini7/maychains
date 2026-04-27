# Polymers in Solvent

In this tutorial you will set up a simulation of 100 polymer chains in an implicit solvent. 

## Step 0. Generate input files for lammps

Following the previous tutorial create a *periodic* simulation box containing *100 polymer chains* each made of *50 monomers*. As in the previous example we are not considering any chemical specificity.

The polymers will be described by:

* Fene bonds
* Mass = 1
* Charge = 0
* Shifted LJ potential (\sigma=1, \epsilon=1)

## Step 1. Initialization

It may be that the beads in the system are overlapping, therefore to avoid instabilities in the simulation, we will perorm an "initialization" run where the *LJ potential* will be substituted by a *soft potential*.
Set the pair coefficient for the soft potential to 1 and scale them up to 30 using the *fix adapt* command copuled with the *ramp* command.
To avoid instabilities caused by bonded interaction run an energy minimization using the *minimize* command. Warning, the bonds in the initial set up files should still be close to the equilibrium value.
Run a *NVT* simulation (*T = 1*) using the langevin dynamics (which includes the solvent effects) employing *fix NVE* and *fix langevin*

* timestep 0.005
* Temperature damping of 0.1
* print output 500 steps
* dump every 1000
* run 500000 steps
* write a data file at the end of the simulation using the *write_data* command

At the end of the simulation visualize the trajectory. What do you notice?
Plot the different curves vs timestep:

* Temperature
* Kinetic Energy
* Potential Energy
* Total energy

Write a comment for each of trend and give an explanation on their behavior. Is it as you expected? Why?

## Step 2. Equilibration

After "initialization", an equilibration run is necessary to allow the system to reach its equilibrium state. The *LJ potential* can now be used as the beads should not be overlapping anymore. To avoid instabilities caused by bonded interaction run an energy minimization using the *minimize* command.

Run an isotropic *NPT* (*P = 0, T = 1*) simulation starting from the end of the initialization to allow the system to reach its equilibrium density using *fix nph* and *fix langevin*

* timestep 0.005
* Temperature damping of 0.1
* Pressure rescaling every 1000 timesteps
* print output 500 steps
* dump every 1000
* run 500000 steps
* write a data file at the end of the simulation using the *write_data* command


At the end of the simulation visualize the trajectory. What do you notice?
Plot the different curves vs timestep:

* Temperature
* Kinetic Energy
* Potential Energy
* Total energy
* Pressure
* Volume 
* Density


Write a comment for each of trend and give an explanation on their behavior comparing it to the initialization step. Is it as you expected? Why?


## Step 3. Production

Starting from the equilibrated system perform a production run. This run will be preformed in the *NVT* ensemble (*T = 1*).
Be Careful! Since the system is now equilibrated, the velocities should not be initialized using the temperature and energy minimization should NOT be performed.

The force-field and thermodynamic settings should not be modified now, or it would mean that the equilibrium state of the system would change as well. The only factors that may be changed are the ones related to time integration.

* timestep 0.005
* Temperature damping of 0.1
* print output 10000 steps
* dump every 2000 steps
* run 10000000 steps
* write a data file at the end of the simulation using the *write_data* command

At the end of the simulation visualize the trajectory. Plot the different curves vs timestep:

* Temperature
* Kinetic Energy
* Potential Energy
* Total energy


Write a comment for each of trend and give an explanation on their behavior comparing it to the equilibration step. Is it as you expected? Why?


## Step 4. Analysis



