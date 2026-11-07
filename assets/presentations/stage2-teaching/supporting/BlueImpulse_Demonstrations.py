#!/usr/bin/env python3
"""Checkable examples used by the Blue Impulse six-chapter teaching module.

Python 3.9+; standard library only. All examples are teaching models.
Run: python3 BlueImpulse_Demonstrations.py --topic all
"""
import argparse
import json


def q_update(old=2.0, alpha=0.5, reward=1.0, gamma=0.9, next_q=4.0, terminal=False):
    """Chapter 2, Update a Q value. A terminal state has no future-value contribution."""
    if not 0 <= alpha <= 1 or not 0 <= gamma <= 1:
        raise ValueError("This example expects alpha and gamma in [0, 1].")
    future = 0.0 if terminal else gamma * next_q
    target = reward + future
    error = target - old
    return dict(old=old, future=future, target=target, error=error,
                change=alpha * error, new=round(old + alpha * error,10), terminal=terminal)


def pipeline(instructions=3):
    """Chapter 3, Overlap work with a pipeline; ideal one-cycle stages, no stalls or hazards."""
    stages = ["Fetch", "Decode", "Execute", "Write"]
    cycles = instructions + len(stages)-1
    rows = []
    for i in range(instructions):
        row = [stages[t-i] if i <= t < i+len(stages) else "-" for t in range(cycles)]
        rows.append(dict(instruction=i+1, cycles=row, completes_at_cycle=i+4))
    return dict(assumptions="Four one-cycle stages; no stalls; independent instructions.",
                rows=rows, pipelined_cycles=cycles, sequential_cycles=instructions*4,
                individual_instruction_cycles=4)


def delay_distances(speed_mps=30.0):
    """Chapter 5, Real-time means meeting a deadline; includes 200 ms practice."""
    if speed_mps < 0:
        raise ValueError("Use a nonnegative speed.")
    return [dict(speed_mps=speed_mps, delay_ms=ms, delay_seconds=ms/1000,
                 distance_metres=speed_mps*ms/1000,
                 meaning="Distance during delay only; not total stopping distance.")
            for ms in [500, 50, 5, 200]]


def accept_message(message, processed_sequence, now_ms=1000):
    """Illustration of Chapter 5, Networking for a behaviour-based agent, not a protocol or a cryptographic implementation.

    authenticated is a supplied result of an EXTERNAL authentication check.
    This function does not authenticate a sender and never controls hardware.
    """
    age=now_ms-message["timestamp_ms"]
    if not message.get("authenticated",False): return "UNAUTHORISED",processed_sequence
    if message.get("device")!="robot-7": return "WRONG DEVICE",processed_sequence
    if message.get("units")!="m": return "WRONG UNITS",processed_sequence
    if message.get("policy_version")!=3: return "WRONG POLICY",processed_sequence
    if age < 0: return "FUTURE TIMESTAMP",processed_sequence
    if age > 200: return "STALE",processed_sequence
    if message["sequence"] <= processed_sequence: return "DUPLICATE / OLD SEQUENCE",processed_sequence
    return "ACCEPT",message["sequence"]


def packet_examples():
    base=dict(device="robot-7",units="m",policy_version=3,authenticated=True)
    examples=[dict(base,sequence=42,timestamp_ms=950),
              dict(base,sequence=43,timestamp_ms=400),
              dict(base,sequence=42,timestamp_ms=940)]
    last=41;result=[]
    for msg in examples:
        status,last=accept_message(msg,last)
        result.append(dict(message=msg,age_ms=1000-msg["timestamp_ms"],
                           result=status,last_processed_sequence=last))
    return dict(assumptions="Illustrative 200 ms limit, robot-7, m, policy 3; authentication checked elsewhere.",
                messages=result,
                learning_note="Match delayed feedback to its original action. Missing feedback is not reward zero.")


def execute_program(add_value=4):
    """Chapter 1, Trace a tiny program; invented teaching ISA, one instruction at each address."""
    program={100:("LOAD",3),101:("ADD",add_value),102:("STORE",200),103:("HALT",None)}
    pc=100;acc=0;memory={200:None};trace=[]
    for _ in range(8):
        mar=pc
        mdr=program[mar]
        pc+=1
        cir=mdr
        op,operand=cir
        before=acc
        if op=="LOAD": acc=operand
        elif op=="ADD": acc+=operand
        elif op=="STORE": memory[operand]=acc
        instruction=op+("" if operand is None else (" #" if op in {"LOAD","ADD"} else " ")+str(operand))
        trace.append(dict(fetched_address=mar, instruction=instruction,
                          PC=pc,MAR=mar,MDR=instruction,CIR=instruction,
                          ACC_before=before,ACC=acc,memory_200=memory[200],
                          transfers=["PC to MAR","memory[MAR] to MDR","advance PC by 1","MDR to CIR","decode","execute"]))
        if op=="HALT":break
    assert memory[200]==3+add_value
    return dict(notation="Invented teaching ISA; # means immediate; STORE uses a destination address.",
                trace=trace, result=memory[200])


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--topic',choices=['all','rl','hardware','network','networked-ai','execution'],default='all')
    p.add_argument('--add',type=int,default=4,help='Change the ADD operand in the execution demonstration.')
    p.add_argument('--speed',type=float,default=30,help='Speed in metres per second for the delay demonstration.')
    p.add_argument('--reward',type=float,default=1,help='Reward in the Q update.')
    a=p.parse_args()
    results={
        'rl':dict(chapter=2,subtopic="Update a Q value",worked=q_update(reward=a.reward),terminal_practice=q_update(terminal=True)),
        'hardware':dict(chapter=3,subtopic="Overlap work with a pipeline",demonstration=pipeline()),
        'network':dict(chapter=5,subtopic="Real-time means meeting a deadline",demonstration=delay_distances(a.speed)),
        'networked-ai':dict(chapter=5,subtopic="Networking for a behaviour-based agent",demonstration=packet_examples()),
        'execution':dict(chapter=1,subtopic="Trace a tiny program",demonstration=execute_program(a.add)),
    }
    print(json.dumps(results if a.topic=='all' else results[a.topic],indent=2))

if __name__=='__main__':main()
