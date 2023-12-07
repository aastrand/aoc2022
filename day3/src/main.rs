use aocrust::io::lines_from_file;
use std::collections::HashSet;
use std::iter::FromIterator;

fn to_priority(item: char) -> u64 {
    let offset = if item.is_lowercase() { 96 } else { 38 };
    (item as u64) - offset
}

fn solve1(filename: &str) -> u64 {
    let input = &lines_from_file(filename);

    let mut sum = 0;
    for r in input {
        let chars = r.chars().collect::<Vec<char>>();

        let p1: HashSet<&char> = HashSet::from_iter(&chars[0..r.len() / 2]);
        let p2 = HashSet::from_iter(&chars[r.len() / 2..]);
        let item = **p1.intersection(&p2).next().unwrap();

        sum += to_priority(item);
    }

    sum as u64
}

fn solve2(filename: &str) -> u64 {
    let input = &lines_from_file(filename);

    let mut sum = 0;
    for i in (0..input.len()).step_by(3) {
        let sacks = &input[i..i + 3];

        // p1 & p2 & p3
        let p1: HashSet<char> = sacks[0].chars().collect();
        let p2: HashSet<char> = sacks[1].chars().collect();
        let p3: HashSet<char> = sacks[2].chars().collect();
        let p4 = p1.intersection(&p2).map(|c| *c).collect::<HashSet<char>>();
        let item = *p4.intersection(&p3).next().unwrap();

        sum += to_priority(item)
    }

    sum
}

fn main() {
    println!("{}", solve1("../input/2022/day3.txt"));
    println!("{}", solve2("../input/2022/day3.txt"));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        assert_eq!(solve1("example.txt"), 157);
    }

    #[test]
    fn test_part2() {
        assert_eq!(solve2("example.txt"), 70);
    }
}
