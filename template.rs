use aocrust::io::lines_from_file;

fn solve1(filename: &str) -> u64 {
    let input = &lines_from_file(filename);

    0
}

fn solve2(filename: &str) -> u64 {
    let input = &lines_from_file(filename);

    0
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
        assert_eq!(solve1("example.txt"), 0);
    }

    #[test]
    fn test_part2() {
        assert_eq!(solve2("example.txt"), 0);
    }
}
