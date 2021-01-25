from os import system, name 
from time import sleep 
import asyncio

global loading
loading = True

def formatnum(num):
  num = round(int(float(num)), 0)
  return str(f"{num:,}")

def clear(): 
  if name == 'nt': 
    _ = system('cls') 
  else: 
    _ = system('clear') 

async def interestcalc(ctype, amount):
  resultcoin = 0
  first = 10000000

  if upgrade[1] == 0:
    second = 5000000
  else:
    second = 10000000

  third = 10000000

  fourth = 20000000

  fifth = 110000000

  if ctype == "personal":
    first = first * 0.2
    second = second * 0.2
    third = third * 0.2
    fourth = fourth * 0.2
    fifth = fifth * 0.2

  if amount > first:
    resultcoin += first * 0.02
    amount -= first
  else:
    resultcoin += amount * 0.02
    return resultcoin,0

  if amount > second:
    resultcoin += second * 0.01
    amount -= second
  else:
    resultcoin += amount * 0.01
    return resultcoin,0

  if amount > third:
    resultcoin += third * 0.005
    amount -= third
  else:
    resultcoin += amount * 0.005
    return resultcoin,0

  if amount > fourth:
    resultcoin += fourth * 0.01
    amount -= fourth
  else:
    resultcoin += amount * 0.01
    return resultcoin,0

  if amount > fifth:
    resultcoin += fifth * 0.005
    amount -= fifth
    return resultcoin,amount
  else:
    resultcoin += amount * 0.005
    return resultcoin,0

async def main():
  global upgrade
  global members
  global total
  track = False
  while track == False:
    print("How much coins in total does your co-op have?")
    total = input()
    try:
      if int(total) <= 0:
        raise Exception
      total = int(total)
    except Exception:
      clear()
      print("Invalid Value!")
    else:
      track = True
  clear()

  track = False
  while track == False:
    print("How many co-op members does your co-op have? (Count yourself as well)")
    members = input()
    try:
      if int(members) == 0 or int(members) > 10:
        raise Exception
      members = int(members)
    except Exception:
      clear()
      print("Invalid Value! (Count yourself as well!)")
    else:
      track = True
  clear()

  track = False
  while track == False:
    print("What is your bank upgrade tier?")
    print("1 | Starter (No Upgrades)")
    print("2 | Gold")
    print("3 | Deluxe")
    print("4 | Super Deluxe")
    print("5 | Premier")
    upgrade = input()
    if upgrade in ["1", "2", "3", "4", "5"]:
      track = True
    else:
      clear()
      print("Invalid value!")
  clear()

  track = False
  while track == False:
    print("How accurate do you want the calculator to be?\n")
    print("Higher accuracies makes the calculator slower, but lets it make less errors")
    print("Lower accuracies are faster, but numbers may be a bit off")
    print("If you have a lot of coins in your bank, you should choose a lower accuracy setting.")
    print("In the future when I rewrite the code, an accuracy setting won't be needed.\n")
    print("1-10 | Very High Accuracy [UNRECOMMENDED]")
    print("11-99 - High Accuracy")
    print("100-200 - Medium Accuracy [RECOMMENDED]")
    print("201+ - Low Accuracy")
    accuracy = input()
    try:
      if int(accuracy) <= 0:
        raise Exception
      accuracy = int(accuracy)
    except Exception:
      clear()
      print("Invalid Value!")
    else:
      track = True
  
  clear()
  print("Calculating...")

  if upgrade == "1":
    upgrade = [0.02, 0 ,0 ,0 ,0 ,15000000 ,3000000]
  elif upgrade == "2":
    upgrade = [0.02, 0.01 , 0, 0, 0, 20000000, 4000000]
  elif upgrade == "3":
    upgrade = [0.02, 0.01 , 0.005, 0, 0, 30000000, 6000000]
  elif upgrade == "4":
    upgrade = [0.02, 0.01 , 0.005, 0.002, 0, 50000000, 10000000]
  elif upgrade == "5":
    upgrade = [0.02, 0.01 , 0.005, 0.002, 0.001, 160000000, 32000000]


  if ((members * upgrade[6]) + (upgrade[5])) <= total:
    coop = upgrade[5]
    personal = upgrade[6]
    remaining = 0
    estimate = (await interestcalc("personal", personal))[0]*members + (await interestcalc("bank", coop))[0]
  else:
    iterates = 0
    personalsum = 0
    coopsum = 0
    while iterates < total:
      personal = (await interestcalc("personal", personalsum + (members*accuracy)))[0] + (await interestcalc("bank", coopsum))[0]
      coop = (await interestcalc("personal", personalsum))[0] + (await interestcalc("bank", coopsum + accuracy))[0]
      if personal > coop:
        iterates += members * accuracy
        personalsum += members * accuracy
      else:
        iterates += accuracy
        coopsum += accuracy
    
    coop = coopsum
    personal = personalsum / members
    estimate = (await interestcalc("personal", personal))[0]*members + (await interestcalc("bank", coop))[0]
    remaining = ((members * upgrade[6]) + (upgrade[5])) - total


  await asyncio.sleep(1)
  clear()
  result = []
  result.append("In order to maximize the amount of interest you get, do the following.\n")
  result.append(f"Put {formatnum(coop)} coins into your Co-Op balance")
  result.append(f"Put {formatnum(personal)} coins into all co-op members' personal bank balances")
  result.append(f"You will earn an estimated amount of {formatnum(estimate)} next interest season.\n")
  if remaining == 0:
    if upgrade != [0.02, 0.01 , 0.005, 0.002, 0.001, 160000000, 32000000]:
      result.append(f"Rerun the calculator if your total coins drops below {formatnum(((members * upgrade[6]) + (upgrade[5])))} coins, or if you upgrade your bank.\n\n")
    else:
      result.append(f"Rerun the calculator if your total coins drops below {formatnum(((members * upgrade[6]) + (upgrade[5])))} coins.\n\n")
  else:
    result.append(f"You need to earn {formatnum(((members * upgrade[6]) + (upgrade[5])))} more coins in order to maximize your interest for the current bank tier.")
    result.append(f"Rerun the calculator again in the next interest season to recalculate the most optimized balances.\n\n")

  result.append("[AD] Join unruled")
  result.append("unurled.gq")

  print('\n'.join(result))

asyncio.run(main())