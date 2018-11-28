from Data import *
from Dependency import *
from Fourlang import *


"""
        //AdjectivePhrase out of one Word
        //NP(JJ(available))
        ADJP -> one_WD(WD)
        [tree] ADJP(?1)
        [ud] ?1
        [fourlang] ?1
"""

#This is the function that generates 2 wide, 1 high NP-s.

def basicUnariADJP():
    result=""

    datas=Data.fromFile("Data/Input/ADJP/adjp_1x1_trees", "Data/Input/ADJP/adjp_1x1_terms", "Data/Input/ADJP/adjp_1x1_deps", 44)
    uniqData={}
    for i in range(len(datas)-1,-1,-1):
        if not (uniqData.keys().__contains__(datas[i].tree.wordLess)):
            uniqData[datas[i].tree.wordLess]=datas[i]

    for input in uniqData.values():
        result+="\n"
        result+="//AdjectivePhrase out of one " + input.words[0].type.Longer + ".\n"
        result+="//" + input.tree.stanford+"\n"
        result+="//" + input.tree.tagTree+"\n"
        result+="ADJP -> one_" + input.words[0].type.Shortest.replace("basic", "") + "(" + input.words[0].type.Shortest + ")\n"
        result+="[string] ?1\n"
        result+="[tree] ADJP(?1)\n"
        result+="[ud] ?1\n"
        result+="[fourlang] ?1\n"
    return result

"""
        //AjdectivePhrase out of a Word1 (whitch is a Modifier1) and a Word2.
        //(ADJP (WD1 stuff) (WD2 stuff))
        ADJP -> mod1_WD1_WD2(WD1, WD2)
        [tree] ADJP2(?1,?2)
        [ud] merge(f_dep(merge("(r<root> :mod1 (d<dep>))", r_dep(?1))),?2)
        [fourlang] merge(f_dep(merge("(r<root> :_ (d<dep>))", r_dep(?1))),?2)
"""

#This is the function that generates 1 wide, 1 high NP-s.

def basicBinaryADJP():
    reverse = False
    connected = False
    sameType = False

    result = ""
    datas = Data.fromFile("Data/Input/ADJP/adjp_1x2_trees", "Data/Input/ADJP/adjp_1x2_terms", "Data/Input/ADJP/adjp_1x2_deps", 209)
    uniqData = {}
    for i in range(len(datas)-1,-1,-1):
        if not (uniqData.keys().__contains__(datas[i].tree.wordLess)):
            uniqData[datas[i].tree.wordLess] = datas[i]

    for input in uniqData.values():
        result+="\n"
        connected = len(input.dependencies) > 1
        sameType = input.words[0].type.Shortest == input.words[1].type.Shortest
        if connected:
            if input.dependencies[1].depType.Shortest == "root":
                input.dependencies[0], input.dependencies[1] = input.dependencies[1], input.dependencies[0]

            reverse = input.words[1].word == input.dependencies[0].endWord

            if not reverse:
                result += ("//AdjectivePhrase out of a " + input.words[0].type.Longer +
                           " (which is a " + input.dependencies[1].depType.Longest +
                           ") and a " + input.words[1].type.Longer + ".\n")
            else:
                result += ("//AdjectivePhrase out of a " + input.words[0].type.Longer +
                           "and a " + input.words[1].type.Longer +
                           " (which is a " + input.dependencies[1].depType.Longest + "). \n")
        else:
            if sameType != sameType:
                result += ("//AdjectivePhrase out of a " + input.words[0].type.Longer + " and a" + input.words[
                    1].type.Longer + ".\n")
            else:
                result += ("//AdjectivePhrase out of two " + input.words[0].type.Longer + "-s.\n")

        result += ("//ADJP2" + input.tree.tagTree[2:] + "\n")
        result += ("//" + input.tree.stanford + "\n")
        if len(input.dependencies) <= 1:
            result += ("ADJP -> undependent_" + input.words[1].type.Shortest.replace("basic", "") +
                   "_" + input.words[0].type.Shortest.replace("basic", "") +
                   "(" + input.words[1].type.Shortest +
                   "," + input.words[0].type.Shortest + ")\n")
        else:
            result += ("ADJP -> "+Digiter.toDigited(input.dependencies[1].depType.Shortest)+"_" + input.words[1].type.Shortest.replace("basic", "") +
                   "_" + input.words[0].type.Shortest.replace("basic", "") +
                   "(" + input.words[1].type.Shortest +
                   "," + input.words[0].type.Shortest + ")\n")


        result+="[string] *(?1,?2)\n"
        result += "[tree] ADJP2(?1,?2)\n"

        reverse = input.words[1].word == input.dependencies[0].endWord
        if connected:
            if not reverse:
                result += ("[ud] merge(f_dep(merge(\"(r<root> :" + input.dependencies[
                    1].depType.Shortest + " (d<dep>))\", r_dep(?2))),?1)\n")
            else:
                result += ("[ud] merge(f_dep(merge(\"(r<root> :" + input.dependencies[
                    1].depType.Shortest + " (d<dep>))\", r_dep(?1))),?2)\n")
        else:
            if not reverse:
                result += ("[ud] ?1\n")
            else:
                result += ("[ud] ?2\n")

        if connected:
            if input.dependencies[1].flangType == Fourlang._None:
                if not reverse:
                    result += ("[fourlang] ?2\n")
                else:
                    result += ("[fourlang] ?1\n")
            elif input.dependencies[1].flangType == Fourlang.OneBack_at_TwoTo:
                if not reverse:
                    result += (
                        "[fourlang] f_dep1(merge(f_dep2(merge(\"(r<root>/AT :1 d1<dep1> :2 (d2<dep2>))\", r_dep2(?2))), r_dep1(?1)))\n")
                else:
                    result += (
                        "[fourlang] f_dep1(merge(f_dep2(merge(\"(r<root>/AT :1 d1<dep1> :2 (d2<dep2>))\", r_dep2(?2))), r_dep1(?2)))\n")
            elif input.dependencies[1].flangType == Fourlang.OneBack_has_TwoTo:
                if not reverse:
                    result += (
                        "[fourlang] f_dep1(merge(f_dep2(merge(\"(r<root>/HAS :1 d1<dep1> :2 (d2<dep2>))\", r_dep2(?2))), r_dep1(?1)))\n")
                else:
                    result += (
                        "[fourlang] f_dep1(merge(f_dep2(merge(\"(r<root>/HAS :1 d1<dep1> :2 (d2<dep2>))\", r_dep2(?1))), r_dep1(?2)))\n")
            elif input.dependencies[1].flangType == Fourlang.OneBack__TwoTo:
                if not reverse:
                    result += (
                        "[fourlang] f_dep1(merge(f_dep2(merge(\"(r<root> :1 d1<dep1> :2 (d2<dep2>))\", r_dep2(?2))), r_dep1(?1)))\n")
                else:
                    result += (
                        "[fourlang] f_dep1(merge(f_dep2(merge(\"(r<root> :1 d1<dep1> :2 (d2<dep2>))\", r_dep2(?1))), r_dep1(?2)))\n")
            elif input.dependencies[1].flangType == Fourlang.OneTo_ZeroBack:
                if not reverse:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :1 (d<dep> :0 (r<root>)))\", r_dep(?2))),?1)\n")
                else:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :1 (d<dep> :0 (r<root>)))\", r_dep(?1))),?2)\n")
            elif input.dependencies[1].flangType == Fourlang.Zero:
                if not reverse:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :0 (d<dep> :0 (r<root>)))\", r_dep(?2))),?1)\n")
                else:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :0 (d<dep> :0 (r<root>)))\", r_dep(?1))),?2)\n")
            elif input.dependencies[1].flangType == Fourlang.ZeroFlat:
                if not reverse:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :0_flat (d<dep>))\", r_dep(?2))),?1)\n")
                else:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :0_flat (d<dep>))\", r_dep(?1))),?2)\n")
            elif input.dependencies[1].flangType == Fourlang.ZeroCompound:
                if not reverse:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :0_compound (d<dep>))\", r_dep(?2))),?1)\n")
                else:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :0_compound (d<dep>))\", r_dep(?1))),?2)\n")
            elif input.dependencies[1].flangType == Fourlang.ZeroTo:
                if not reverse:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :0 (d<dep>))\", r_dep(?2))),?1)\n")
                else:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :0 (d<dep>))\", r_dep(?1))),?2)\n")
            elif input.dependencies[1].flangType == Fourlang.UnderTo:
                if not reverse:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :_ (d<dep>))\", r_dep(?2))),?1)\n")
                else:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :_ (d<dep>))\", r_dep(?1))),?2)\n")
            elif input.dependencies[1].flangType == Fourlang.TwoTo:
                if not reverse:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :2 (d<dep>))\", r_dep(?2))),?1)\n")
                else:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :2 (d<dep>))\", r_dep(?1))),?2)\n")
            else:
                if not reverse:
                    result += ("[fourlang] ?1\n")
                else:
                    result += ("[fourlang] ?2\n")
        else:
            if not reverse:
                result += ("[fourlang] ?1\n")
            else:
                result += ("[fourlang] ?2\n")
    return result


"""
1. Reading in the data
2. format the wordless trees
3. clean data from redundancy
4. sort the data into categories
5. generate the right text depending on the category
ADJP( JJ( ), JJ( ), JJS( ))
"""

#This is the function that generates 3 wide, 1 high NP-s.

def basicTernaryADJPTail():
    reverse = False
    connected = False
    sameType = False

    result = ""
    datas = Data.fromFile("Data/Input/ADJP/adjp_1x3_trees", "Data/Input/ADJP/adjp_1x3_terms", "Data/Input/ADJP/adjp_1x3_deps", 45)
    for input in datas:
        tmp=input.tree.wordLess.split(" ")
        input.tree.wordLess=tmp[0]+" ...( "+tmp[2]+" "+tmp[3]+" "+tmp[4]+" "+tmp[5]+" "+tmp[6]
    uniqData = {}
    for i in range(len(datas)-1,-1,-1):
        if not (uniqData.keys().__contains__(datas[i].tree.wordLess)):
            uniqData[datas[i].tree.wordLess] = datas[i]

    for input in uniqData.values():

        input.words.remove(input.words[2])

        place=-1
        for index in range(0,len(input.dependencies)):
            if ((input.dependencies[index].startWord == input.words[0].word and input.dependencies[index].endWord == input.words[1].word)
                    or (input.dependencies[index].startWord == input.words[1].word and input.dependencies[index].endWord == input.words[0].word)):
                place=index

        if place != -1:
            input.dependencies=[input.dependencies[place]]
        else:
            input.dependencies=[]

        result+="\n"
        connected = len(input.dependencies) ==1
        sameType = input.words[0].type.Shortest == input.words[1].type.Shortest
        if connected:
            reverse = input.words[1].word == input.dependencies[0].startWord

            if not reverse:
                result += ("//End of a AdjectivePhrase out of a " + input.words[1].type.Longer +
                           " (which is a " + input.dependencies[0].depType.Longest +
                           ") and a " + input.words[0].type.Longer + ".\n")
            else:
                result += ("//End of a AdjectivePhrase End out of a " + input.words[1].type.Longer +
                           "and a " + input.words[0].type.Longer +
                           " (which is a " + input.dependencies[0].depType.Longest + "). \n")
        else:
            if sameType != sameType:
                result += ("//End of a AdjectivePhrase End out of a " + input.words[1].type.Longer +
                           " and a" + input.words[0].type.Longer + ".\n")
            else:
                result += ("//End of a NounPhrase End out of two " + input.words[0].type.Longer + "-s.\n")

        result += ("//ADJP3" + input.tree.tagTree[2:] + "\n")
        result += ("//" + input.tree.stanford + "\n")
        if len(input.dependencies)==1:
            result += ("ADJP_BAR -> "+Digiter.toDigited(input.dependencies[0].depType.Shortest)+"_" + input.words[1].type.Shortest.replace("basic", "") +
                   "_" + input.words[0].type.Shortest.replace("basic", "") +
                   "_Tail(" + input.words[1].type.Shortest +
                   "," + input.words[0].type.Shortest + ")\n")
        else:
            result += ("ADJP_BAR -> undependent_" + input.words[1].type.Shortest.replace("basic", "") +
                   "_" + input.words[0].type.Shortest.replace("basic", "") +
                   "_Tail(" + input.words[1].type.Shortest +
                   "," + input.words[0].type.Shortest + ")\n")

        result+="[string] *(?1,?2)\n"
        result += "[tree] ADJP3(*,?1,?2)\n"

        if connected:
            if not reverse:
                result += ("[ud] merge(f_dep(merge(\"(r<root> :" + input.dependencies[
                    0].depType.Shortest + " (d<dep>))\", r_dep(?2))),?1)\n")
            else:
                result += ("[ud] merge(f_dep(merge(\"(r<root> :" + input.dependencies[
                    0].depType.Shortest + " (d<dep>))\", r_dep(?1))),?2)\n")
        else:
            if not reverse:
                result += ("[ud] ?1\n")
            else:
                result += ("[ud] ?2\n")

        if connected:
            if input.dependencies[0].flangType == Fourlang._None:
                if not reverse:
                    result += ("[fourlang] ?2\n")
                else:
                    result += ("[fourlang] ?1\n")
            elif input.dependencies[0].flangType == Fourlang.OneBack_at_TwoTo:
                if not reverse:
                    result += (
                        "[fourlang] f_dep1(merge(f_dep2(merge(\"(r<root>/AT :1 d1<dep1> :2 (d2<dep2>))\", r_dep2(?2))), r_dep1(?1)))\n")
                else:
                    result += (
                        "[fourlang] f_dep1(merge(f_dep2(merge(\"(r<root>/AT :1 d1<dep1> :2 (d2<dep2>))\", r_dep2(?2))), r_dep1(?2)))\n")
            elif input.dependencies[0].flangType == Fourlang.OneBack_has_TwoTo:
                if not reverse:
                    result += (
                        "[fourlang] f_dep1(merge(f_dep2(merge(\"(r<root>/HAS :1 d1<dep1> :2 (d2<dep2>))\", r_dep2(?2))), r_dep1(?1)))\n")
                else:
                    result += (
                        "[fourlang] f_dep1(merge(f_dep2(merge(\"(r<root>/HAS :1 d1<dep1> :2 (d2<dep2>))\", r_dep2(?1))), r_dep1(?2)))\n")
            elif input.dependencies[0].flangType == Fourlang.OneBack__TwoTo:
                if not reverse:
                    result += (
                        "[fourlang] f_dep1(merge(f_dep2(merge(\"(r<root> :1 d1<dep1> :2 (d2<dep2>))\", r_dep2(?2))), r_dep1(?1)))\n")
                else:
                    result += (
                        "[fourlang] f_dep1(merge(f_dep2(merge(\"(r<root> :1 d1<dep1> :2 (d2<dep2>))\", r_dep2(?1))), r_dep1(?2)))\n")
            elif input.dependencies[0].flangType == Fourlang.OneTo_ZeroBack:
                if not reverse:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :1 (d<dep> :0 (r<root>)))\", r_dep(?2))),?1)\n")
                else:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :1 (d<dep> :0 (r<root>)))\", r_dep(?1))),?2)\n")
            elif input.dependencies[0].flangType == Fourlang.Zero:
                if not reverse:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :0 (d<dep> :0 (r<root>)))\", r_dep(?2))),?1)\n")
                else:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :0 (d<dep> :0 (r<root>)))\", r_dep(?1))),?2)\n")
            elif input.dependencies[0].flangType == Fourlang.ZeroFlat:
                if not reverse:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :0_flat (d<dep>))\", r_dep(?2))),?1)\n")
                else:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :0_flat (d<dep>))\", r_dep(?1))),?2)\n")
            elif input.dependencies[0].flangType == Fourlang.ZeroCompound:
                if not reverse:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :0_compound (d<dep>))\", r_dep(?2))),?1)\n")
                else:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :0_compound (d<dep>))\", r_dep(?1))),?2)\n")
            elif input.dependencies[0].flangType == Fourlang.ZeroTo:
                if not reverse:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :0 (d<dep>))\", r_dep(?2))),?1)\n")
                else:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :0 (d<dep>))\", r_dep(?1))),?2)\n")
            elif input.dependencies[0].flangType == Fourlang.UnderTo:
                if not reverse:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :_ (d<dep>))\", r_dep(?2))),?1)\n")
                else:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :_ (d<dep>))\", r_dep(?1))),?2)\n")
            elif input.dependencies[0].flangType == Fourlang.TwoTo:
                if not reverse:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :2 (d<dep>))\", r_dep(?2))),?1)\n")
                else:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :2 (d<dep>))\", r_dep(?1))),?2)\n")
            else:
                if not reverse:
                    result += ("[fourlang] ?1\n")
                else:
                    result += ("[fourlang] ?2\n")
        else:
            if not reverse:
                result += ("[fourlang] ?1\n")
            else:
                result += ("[fourlang] ?2\n")
    return result
"""
ADJP( JJ( ), JJ( ), jj( ))
"""
def basicTernaryADJPComplete():
    reverse = False
    connected = False

    result = ""
    datas = Data.fromFile("Data/Input/ADJP/adjp_1x3_trees", "Data/Input/ADJP/adjp_1x3_terms", "Data/Input/ADJP/adjp_1x3_deps", 45)
    for input in datas:
        tmp=input.tree.wordLess.split(" ")
        input.tree.wordLess=tmp[0]+" "+tmp[1]+" "+tmp[2]+" ...( "+tmp[4]+" ...( "+tmp[6]
    uniqData = {}
    for i in range(len(datas)-1,-1,-1):
        if not (uniqData.keys().__contains__(datas[i].tree.wordLess)):
            uniqData[datas[i].tree.wordLess] = datas[i]

    for input in uniqData.values():

        input.words.remove(input.words[1])
        input.words.remove(input.words[0])

        place=-1
        for index in range(0,len(input.dependencies)):
            if ((input.dependencies[index].startWord == input.words[0].word or input.dependencies[index].endWord == input.words[0].word)):
                place=index
                break

        if place != -1:
            input.dependencies=[input.dependencies[place]]
        else:
            input.dependencies=[]

        if(len(input.dependencies)==0 or input.dependencies[0].depType.Shortest=="root"):
            print("root")

        result+="\n"
        connected = len(input.dependencies) == 1
        if connected:
            reverse = input.words[0].word == input.dependencies[0].endWord

            if not reverse:
                result += ("//a long AdjectivePhrase out of a " + input.words[0].type.Longer +
                           " (which is a " + input.dependencies[0].depType.Longest +
                           ") and a AdjectivePhrase Bar.\n")
            else:
                result += ("//a long AdjectivePhrase out of a  AdjectivePhrase Bar and a " + input.words[0].type.Longer +
                           " (which is a " + input.dependencies[0].depType.Longest + "). \n")
        else:
            result += ("//a long AdjectivePhrase out of a " + input.words[0].type.Longer +
                       " and a AdjectivePhrase Bar.\n")

        result += ("//ADJP3" + input.tree.tagTree[2:] + "\n")
        result += ("//" + input.tree.stanford + "\n")
        if len(input.dependencies)==1:
            result += ("ADJP -> "+Digiter.toDigited(input.dependencies[0].depType.Shortest)+"_" + input.words[0].type.Shortest.replace("basic", "") +
                   "_ADJPBAR_Tail(" + input.words[0].type.Shortest +
                   ", ADJP_BAR)\n")
        else:
            result += ("ADJP -> unconnected_" + input.words[0].type.Shortest.replace("basic", "") +
                   "_ADJPBAR(" + input.words[0].type.Shortest +
                   ", ADJP_BAR)\n")

        result+="[string] *(?1,?2)\n"
        result += "[tree] @(?2,?1)\n"

        if connected:
            if not reverse:
                result += ("[ud] merge(f_dep(merge(\"(r<root> :" + input.dependencies[
                    0].depType.Shortest + " (d<dep>))\", r_dep(?2))),?1)\n")
            else:
                result += ("[ud] merge(f_dep(merge(\"(r<root> :" + input.dependencies[
                    0].depType.Shortest + " (d<dep>))\", r_dep(?1))),?2)\n")
        else:
            if not reverse:
                result += ("[ud] ?1\n")
            else:
                result += ("[ud] ?2\n")

        if connected:
            if input.dependencies[0].flangType == Fourlang._None:
                if not reverse:
                    result += ("[fourlang] ?2\n")
                else:
                    result += ("[fourlang] ?1\n")
            elif input.dependencies[0].flangType == Fourlang.OneBack_at_TwoTo:
                if not reverse:
                    result += (
                        "[fourlang] f_dep1(merge(f_dep2(merge(\"(r<root>/AT :1 d1<dep1> :2 (d2<dep2>))\", r_dep2(?2))), r_dep1(?1)))\n")
                else:
                    result += (
                        "[fourlang] f_dep1(merge(f_dep2(merge(\"(r<root>/AT :1 d1<dep1> :2 (d2<dep2>))\", r_dep2(?2))), r_dep1(?2)))\n")
            elif input.dependencies[0].flangType == Fourlang.OneBack_has_TwoTo:
                if not reverse:
                    result += (
                        "[fourlang] f_dep1(merge(f_dep2(merge(\"(r<root>/HAS :1 d1<dep1> :2 (d2<dep2>))\", r_dep2(?2))), r_dep1(?1)))\n")
                else:
                    result += (
                        "[fourlang] f_dep1(merge(f_dep2(merge(\"(r<root>/HAS :1 d1<dep1> :2 (d2<dep2>))\", r_dep2(?1))), r_dep1(?2)))\n")
            elif input.dependencies[0].flangType == Fourlang.OneBack__TwoTo:
                if not reverse:
                    result += (
                        "[fourlang] f_dep1(merge(f_dep2(merge(\"(r<root> :1 d1<dep1> :2 (d2<dep2>))\", r_dep2(?2))), r_dep1(?1)))\n")
                else:
                    result += (
                        "[fourlang] f_dep1(merge(f_dep2(merge(\"(r<root> :1 d1<dep1> :2 (d2<dep2>))\", r_dep2(?1))), r_dep1(?2)))\n")
            elif input.dependencies[0].flangType == Fourlang.OneTo_ZeroBack:
                if not reverse:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :1 (d<dep> :0 (r<root>)))\", r_dep(?2))),?1)\n")
                else:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :1 (d<dep> :0 (r<root>)))\", r_dep(?1))),?2)\n")
            elif input.dependencies[0].flangType == Fourlang.Zero:
                if not reverse:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :0 (d<dep> :0 (r<root>)))\", r_dep(?2))),?1)\n")
                else:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :0 (d<dep> :0 (r<root>)))\", r_dep(?1))),?2)\n")
            elif input.dependencies[0].flangType == Fourlang.ZeroFlat:
                if not reverse:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :0_flat (d<dep>))\", r_dep(?2))),?1)\n")
                else:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :0_flat (d<dep>))\", r_dep(?1))),?2)\n")
            elif input.dependencies[0].flangType == Fourlang.ZeroCompound:
                if not reverse:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :0_compound (d<dep>))\", r_dep(?2))),?1)\n")
                else:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :0_compound (d<dep>))\", r_dep(?1))),?2)\n")
            elif input.dependencies[0].flangType == Fourlang.ZeroTo:
                if not reverse:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :0 (d<dep>))\", r_dep(?2))),?1)\n")
                else:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :0 (d<dep>))\", r_dep(?1))),?2)\n")
            elif input.dependencies[0].flangType == Fourlang.UnderTo:
                if not reverse:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :_ (d<dep>))\", r_dep(?2))),?1)\n")
                else:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :_ (d<dep>))\", r_dep(?1))),?2)\n")
            elif input.dependencies[0].flangType == Fourlang.TwoTo:
                if not reverse:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :2 (d<dep>))\", r_dep(?2))),?1)\n")
                else:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :2 (d<dep>))\", r_dep(?1))),?2)\n")
            else:
                if not reverse:
                    result += ("[fourlang] ?1\n")
                else:
                    result += ("[fourlang] ?2\n")
        else:
            if not reverse:
                result += ("[fourlang] ?1\n")
            else:
                result += ("[fourlang] ?2\n")
    return result
