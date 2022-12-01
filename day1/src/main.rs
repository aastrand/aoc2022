use aocrust::io::from_file;

fn solve1(filename: &str) -> u64 {
    let input = &from_file(filename);

    input
        .trim()
        .split("\n\n")
        .map(|s| s.split("\n").map(|i| i.parse::<u64>().unwrap()).sum())
        .max()
        .unwrap()
}

fn solve2(filename: &str) -> u64 {
    let input = &from_file(filename);

    let mut elves = input
        .trim()
        .split("\n\n")
        .map(|s| s.split("\n").map(|i| i.parse::<u64>().unwrap()).sum())
        .collect::<Vec<u64>>();

    elves.sort_by(|a, b| b.cmp(a));

    return elves[0] + elves[1] + elves[2];
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
        assert_eq!(solve1("example.txt"), 24000);
    }

    #[test]
    fn test_part2() {
        assert_eq!(solve2("example.txt"), 45000);
    }
}
