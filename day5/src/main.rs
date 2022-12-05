use aocrust::io::from_file;
use aocrust::parse::ints;
use regex::Regex;

fn parse(input: &str) -> (Vec<Vec<&str>>, Vec<&str>) {
    let parts: Vec<&str> = input.split("\n\n").collect();

    let mut stack_input = parts[0].split("\n").collect::<Vec<&str>>();
    stack_input.reverse();

    let size = stack_input[0].trim().chars().last().unwrap() as usize - 48;
    let re = r"(\[[A-Z]\]|   ) (\[[A-Z]\]|   ) (\[[A-Z]\]|   )[ ]?(\[[A-Z]\]|   |)[ ]?(\[[A-Z]\]|   |)[ ]?(\[[A-Z]\]|   |)[ ]?(\[[A-Z]\]|   |)[ ]?(\[[A-Z]\]|   |)[ ]?(\[[A-Z]\]|   |)";
    let mut stacks: Vec<Vec<&str>> = vec![];
    for _i in 0..size {
        stacks.push(vec![]);
    }

    let regex = Regex::new(&re).unwrap();
    for row in &stack_input[1..] {
        let captures = regex.captures(row).unwrap();
        for i in 0..stacks.len() {
            if let Some(v) = captures.get(i + 1) {
                if v.as_str().contains("[") {
                    stacks[i].push(&v.as_str()[1..2]);
                }
            }
        }
    }

    (stacks, parts[1].trim().split("\n").collect::<Vec<&str>>())
}

fn answer(stacks: &Vec<Vec<&str>>) -> String {
    let mut r = String::new();
    for s in stacks {
        r.push_str(s.last().unwrap_or(&""));
    }
    r
}

fn solve1(filename: &str) -> String {
    let input = &from_file(filename);
    let (mut stacks, instructions) = parse(input);

    for instr in instructions {
        let idx = ints(instr);
        for _c in 0..idx[0] {
            let moved = stacks[(idx[1] - 1) as usize].pop().unwrap();
            stacks[(idx[2] - 1) as usize].push(moved);
        }
    }

    answer(&stacks)
}

fn solve2(filename: &str) -> String {
    let input = &from_file(filename);
    let (mut stacks, instructions) = parse(input);

    for instr in instructions {
        let idx = ints(instr);
        let mut tmp = vec![];
        for _c in 0..idx[0] {
            let moved = stacks[(idx[1] - 1) as usize].pop().unwrap();
            tmp.push(moved);
        }
        for _i in 0..tmp.len() {
            stacks[(idx[2] - 1) as usize].push(tmp.pop().unwrap());
        }
    }

    answer(&stacks)
}

fn main() {
    println!("{}", solve1("input.txt"));
    println!("{}", solve2("input.txt"));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        assert_eq!(solve1("example.txt"), "CMZ");
    }

    #[test]
    fn test_part2() {
        assert_eq!(solve2("example.txt"), "MCD");
    }
}
